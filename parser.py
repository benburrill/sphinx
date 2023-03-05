import operator
from collections import ChainMap, deque
import expressions as expr
import directives as direc
from context import output_map
from memory import MemoryFormat
from program import Program, CodeTable
import re
import sys

from errors import *


class Scanner:
    def __init__(self, string, *, file=None, line=1):
        self.string = string
        self.file = file
        self.line = line
        self.pos = 0

    def read(self, pat):
        mo = pat.match(self.string, self.pos)
        if mo is not None:
            self.pos = mo.end()
            return mo.group()
        return None

    def read_tok(self, tok_pat):
        mo = tok_pat.match(self.string, self.pos)
        if mo is not None:
            self.pos = mo.end()
            return (mo.lastgroup, mo.group())
        return None

    def read_chars(self, count=1):
        result = self.string[self.pos:self.pos+count]
        self.pos += len(result)
        return result

    def read_string(self, string):
        length = len(string)
        if self.string[self.pos:self.pos+length] == string:
            self.pos += length
            return True
        return False

    def __bool__(self):
        # Is there any more to read?
        return self.pos < len(self.string)

    def get_origin(self):
        return Origin(file=self.file, line=self.line, column=self.pos)

    def __repr__(self):
        return f'Scanner({self.string[self.pos:]!r})'



anything = re.compile(rb'[^\s;]+')
ignore = re.compile(rb'\s*(?:;.*)?', re.DOTALL)

def is_end(scan):
    scan.read(ignore)
    return not bool(scan)


# Based on the example from https://docs.python.org/3/library/re.html
def tok_re(spec):
    return '|'.join(f'(?P<{name}>{re})' for name, re in spec.items())


esc_codes = dict([b'a\a', b'b\b', b'f\f', b'n\n', b'r\r', b't\t', b'0\0', b"''", b'""', rb'\\'])
esc_code_tok = re.compile(tok_re({
    'hex': r'x[\da-fA-F]{2}',
    'code': '[abfnrt0\'"\\\\]'
}).encode())

def read_escape_code(scan):
    match scan.read_tok(esc_code_tok):
        case ('hex', val):
            return int(val[1:], base=16)
        case ('code', code):
            return esc_codes[code[0]]
    raise AssemblerSyntaxError('Invalid escape sequence', scan.get_origin())


string_tok = re.compile(tok_re({
    'bytes': r'[^\\"]+',
    'escape': r'\\',
    'end': '"'
}).encode())
def read_string_literal(scan):
    if not scan.read_string(b'"'):
        return None

    result = b''
    while scan:
        match scan.read_tok(string_tok):
            case ('bytes', val):
                result += val
            case ('escape', _):
                result += bytes([read_escape_code(scan)])
            case ('end', _):
                return result

    raise AssemblerSyntaxError('Unterminated string literal', scan.get_origin())




num_literal_tok = re.compile(tok_re({
    'hex': r'0x[\da-fA-F][\da-fA-F_]*',
    'oct': r'0o[0-7][0-7_]*',
    'bin': r'0b[01][01_]*',
    'dec': r'\d[\d_]*',
    'char': r"'[^'\\]'",
    'char_escape_start': r"'\\"
}).encode())

def read_word_suffix(scan, ex, mf):
    if mf is None:
        return ex

    if scan.read_string(b'w'):
        return expr.WordScaled(ex, mf)

    return ex

def read_num_literal(scan, mf=None):
    match scan.read_tok(num_literal_tok):
        case ('hex', val):
            return read_word_suffix(scan, expr.Value(int(val, base=16)), mf)
        case ('oct', val):
            return read_word_suffix(scan, expr.Value(int(val, base=8)), mf)
        case ('bin', val):
            return read_word_suffix(scan, expr.Value(int(val, base=2)), mf)
        case ('dec', val):
            return read_word_suffix(scan, expr.Value(int(val, base=10)), mf)
        case ('char', val):
            return expr.Value(val[1])
        case ('char_escape_start', _):
            seq = read_escape_code(scan)
            scan.read_string(b"'")
            return expr.Value(seq)
    return None


ident_re = r'[a-zA-Z_]\w*'
ident_pat = re.compile(ident_re.encode())
direc_pat = re.compile(rb'[a-zA-Z_.]\w*')

expr_ops = re.compile(rb'[()+\-*/]')

def read_expression_tokens(scan, namespace, mf):
    while scan:
        scan.read(ignore)
        op = scan.read(expr_ops)
        if op is not None:
            yield op.decode(), scan.get_origin()

        ident = scan.read(ident_pat)
        if ident is not None:
            yield expr.Variable(scan.get_origin(), namespace, ident.decode()), scan.get_origin()

        lit = read_num_literal(scan, mf)
        if lit is not None:
            yield lit, scan.get_origin()

        if not (op or ident or lit):
            break


prec = {'+': 0, '-': 0, '*': 1, '/': 1, 'u+': 2, 'u-': 2}
op_table = {'+': operator.add, '-': operator.sub,
            '*': operator.mul, '/': operator.floordiv,
            'u+': operator.pos, 'u-': operator.neg}

def push_op(rpn, info):
    tok, origin = info
    try:
        if tok.startswith('u'):
            arg = rpn.pop()
            rpn.append(expr.Operation(origin, tok[1:], op_table[tok], [arg]))
        else:
            right = rpn.pop()
            left = rpn.pop()
            rpn.append(expr.Operation(origin, tok, op_table[tok], [left, right]))
    except IndexError:
        raise AssemblerSyntaxError.unhelpful(origin)


def shunt(tokens):
    rpn = deque()
    ops = deque()
    expr_prev = False

    for tok, origin in tokens:
        if not expr_prev:
            if tok == '+':
                tok = 'u+'
            elif tok == '-':
                tok = 'u-'
        if tok == '(':
            ops.append((tok, origin))
        elif tok == ')':
            while ops:
                top = ops.pop()
                if top[0] == '(':
                    break
                push_op(rpn, top)
            else:
                raise AssemblerSyntaxError('No matching opening parenthesis', origin)
            expr_prev = True
            continue
        elif tok in prec:
            while ops and ops[-1][0] != '(':
                if prec[ops[-1][0]] < prec[tok]:
                    break
                if ops[-1][0][0] == tok[0] == 'u':
                    break
                push_op(rpn, ops.pop())
            ops.append((tok, origin))
        else:
            expr_prev = True
            rpn.append(tok)
            continue
        expr_prev = False

    while ops:
        push_op(rpn, ops.pop())

    result = rpn.pop()

    if rpn:
        raise AssemblerSyntaxError.unhelpful(origin)

    return result


def expect_expression(scan, namespace, mf):
    tok = list(read_expression_tokens(scan, namespace, mf))
    if not tok:
        raise AssemblerSyntaxError(
            'Expected expression',
            scan.get_origin()
        )

    return shunt(tok)


# for data directives like .word 1,2,3,4,5
def read_multi_expr(scan, namespace, mf):
    while scan:
        yield expect_expression(scan, namespace, mf)
        scan.read(ignore)

        if not scan.read_string(b','):
            break


def read_instr_var(scan, namespace, mf):
    scan.read(ignore)
    if scan.read_string(b'['):
        ex = expect_expression(scan, namespace, mf)
        scan.read(ignore)
        if scan.read_string(b']'):
            return expr.Tagged('sv', ex)
    elif scan.read_string(b'{'):
        ex = expect_expression(scan, namespace, mf)
        scan.read(ignore)
        if scan.read_string(b'}'):
            return expr.Tagged('cv', ex)
    else:
        return expr.Tagged('im', expect_expression(scan, namespace, mf))

    raise AssemblerSyntaxError.unhelpful(scan.get_origin())


arg_spec_name = re.compile(rb':\w+:')
whitespace = re.compile(rb'\s+')

def expect_space(scan):
    if scan.read(whitespace) is None:
        if is_end(scan):
            raise AssemblerSyntaxError('Expected argument', scan.get_origin())

        raise AssemblerSyntaxError('Expected space', scan.get_origin())


def read_args(scan, arg_string, namespace, mf):
    arg_scan = Scanner(arg_string)
    while arg_scan:
        need = arg_scan.read(arg_spec_name) or arg_scan.read_chars(1)

        # Significant whitespace
        if need == b' ':
            expect_space(scan)
            continue

        # Note: is_end does read(ignore) for us
        if is_end(scan):
            if need == b',':
                raise AssemblerSyntaxError(
                    'Expected additional arguments, but found end of argument list',
                    scan.get_origin()
                )
            raise AssemblerSyntaxError(
                f'Expected {need.decode()}, but found end of argument list',
                scan.get_origin()
            )

        match need:
            case b':expr:':
                yield expect_expression(scan, namespace, mf)
            case b':ident:':
                ident = scan.read(ident_pat)
                if ident is None:
                    raise AssemblerSyntaxError('Expected identifier', scan.get_origin())
                yield expr.Value(ident.decode())
            case b':inst_arg:':
                yield read_instr_var(scan, namespace, mf)
            case b':multi_expr:':
                yield from read_multi_expr(scan, namespace, mf)
            case b':string:':
                lit = read_string_literal(scan)
                if lit is None:
                    raise AssemblerSyntaxError('Expected string literal', scan.get_origin())
                yield expr.Value(lit)
            case _:
                if not scan.read_string(need):
                    raise AssemblerSyntaxError(
                        f'Invalid argument syntax, expected {need.decode()}',
                        scan.get_origin()
                    )

    if not is_end(scan):
        if scan.read_string(b','):
            raise AssemblerSyntaxError('Too many arguments', scan.get_origin())

        raise AssemblerSyntaxError.unhelpful(scan.get_origin())


instr_table = [
    (set('halt'.split('|')),
     b''),
    (set('j|yield'.split('|')), 
     b' :inst_arg:'),
    (set('hgt|hlt|heq|hne|hge|hle|sws|sbs'.split('|')),
     b' :inst_arg:,:inst_arg:'),
    (set('mov|lws|lwc|lbs|lbc'.split('|')),
     b' [:expr:],:inst_arg:'),
    (set('add|sub|mul|div|mod|lwso|lwco|lbso|lbco'.split('|')),
     b' [:expr:],:inst_arg:,:inst_arg:'),
    (set('swso|sbso'.split('|')),
     b' :inst_arg:,:inst_arg:,:inst_arg:'),
    (set('flag'.split('|')),
     b' :ident:')
]

def read_instruction(scan, namespace, mf):
    instr_name = scan.read(direc_pat)
    if instr_name is None: raise AssemblerSyntaxError.unhelpful(scan.get_origin())
    instr_name = instr_name.decode()

    for instrs, args in instr_table:
        if instr_name in instrs:
            return direc.InstructionDirective(instr_name, list(read_args(scan, args, namespace, mf)))

    raise AssemblerSyntaxError(f'{instr_name} is not an instruction', scan.get_origin())


def read_data_direc(scan, namespace, mf):
    direc_name = scan.read(direc_pat)
    if direc_name is None: raise AssemblerSyntaxError.unhelpful(scan.get_origin())
    direc_name = direc_name.decode()

    match direc_name:
        case '.ascii':
            string_expr, = read_args(scan, b' :string:', namespace, mf)
            return direc.AsciiDirective(string_expr.get())
        case '.asciiz':
            string_expr, = read_args(scan, b' :string:', namespace, mf)
            return direc.AsciiDirective(string_expr.get() + b'\0')
        case '.word':
            word_exprs = list(read_args(scan, b' :multi_expr:', namespace, mf))
            return direc.WordDirective(word_exprs, mf)
        case '.byte':
            byte_exprs = list(read_args(scan, b' :multi_expr:', namespace, mf))
            return direc.ByteDirective(byte_exprs)
        case '.fill':
            fill_expr, length_expr = read_args(scan, b' :expr:,:expr:', namespace, mf)
            return direc.FillDirective(fill_expr, length_expr, scan.get_origin())
        case '.zero':
            length_expr, = read_args(scan, b' :expr:', namespace, mf)
            return direc.FillDirective(expr.Value(0), length_expr, scan.get_origin())
        case _:
            raise AssemblerSyntaxError(
                f'{direc_name} is not a data directive',
                scan.get_origin()
            )


meta_tok = re.compile(tok_re({
    'label': rf'{ident_re}:',
    'preproc': r'%'
}).encode())

class Parser:
    def __init__(self):
        self.sources = {}
        self.globals = {}
        self.format = {}
        self.sections = {'code': [], 'const': [], 'state': []}

        # The actual initial word size doesn't matter here, we just need
        # a shared MemoryFormat to pass around to expressions even it
        # doesn't have a concrete value yet.
        self.mf = MemoryFormat(2)

    def get_program(self):
        self.mf.set_word_size(self.format.get('word', 2))
        return Program(
            mf=self.mf.copy(), pc=0,
            code=CodeTable(tuple([d.get() for d in self.sections['code']])),
            const=b''.join([d.get() for d in self.sections['const']]),
            state=memoryview(bytearray().join(
                [d.get() for d in self.sections['state']]
            ))
        )

    def get_output_context(self):
        return output_map[self.format.get('output', 'signed')]()

    def read_section(self, scan):
        section = scan.read(ident_pat)

        if section is None or not is_end(scan):
            raise AssemblerSyntaxError.unhelpful(scan.get_origin())

        section = section.decode()

        if section not in self.sections:
            raise AssemblerSyntaxError(
                f'Section must be one of {list(self.sections)!r}, '
                f'not {section}',
                scan.get_origin()
            )

        return section

    def read_format_spec(self, scan):
        match scan.read(ident_pat):
            case b'word':
                expect_space(scan)
                if scan.read_string(b'inf'):
                    size = 'inf'
                else:
                    size = read_num_literal(scan)
                    if size is None or size.get() <= 0:
                        raise AssemblerSyntaxError(
                            'Invalid word size: must be positive integer or inf',
                            scan.get_origin()
                        )

                    size = size.get()

                return ('word', size)

            case b'output':
                expect_space(scan)
                output = scan.read(ident_pat)
                if output is None:
                    raise AssemblerSyntaxError.unhelpful(scan.get_origin())

                output = output.decode()

                if output not in output_map:
                    raise AssemblerSyntaxError(
                        f'Invalid output format: {output}, must be in '
                        f'{list(output_map)}',
                        scan.get_origin()
                    )

                return ('output', output)

            case None:
                raise AssemblerSyntaxError.unhelpful(scan.get_origin())

            case bad_spec:
                raise AssemblerSyntaxError(
                    f'Invalid format specifier {bad_spec.decode()}',
                    scan.get_origin()
                )


    def prepare_section(self, section):
        # Add halt to end of previous code section if it exists
        if section == 'code' and self.sections['code']:
            self.sections['code'].append(direc.InstructionDirective('halt', []))


    def handle_error(self, err):
        print('Assembler error:')
        while err is not None:
            if isinstance(err, AssemblerError):
                print(err, file=sys.stderr)
                origin = err.origin
                print(f'    File {origin.file!r}, line {origin.line}', file=sys.stderr)
                print(f'    > {self.sources[origin.file][origin.line-1].decode().strip()}', file=sys.stderr)
            else:
                print(f'{type(err).__name__}: {err}')

            err = err.__cause__


    def parse_file(self, fname):
        with open(fname, 'rb') as file:
            return self.parse_lines(file.readlines(), fname)

    def parse_lines(self, lines, file=None):
        if file is None:
            file = '<unknown>'

        self.sources[file] = lines

        section = 'code'
        self.prepare_section(section)
        # TODO: I don't think globals should work with the ChainMap as I
        # had earlier, but I'm not entirely sure how it should work.
        # I guess %extern something could do 
        # namespace['something'] = Variable(origin, self.globals, 'something')
        # Or we could do the ChainMap, but not to self.globals, but our
        # own globals... but then what?
        namespace = {} # ChainMap({}, self.globals)

        for line_number, line in enumerate(lines, start=1):
            scan = Scanner(line, file=file, line=line_number)
            while scan:
                scan.read(ignore)

                match scan.read_tok(meta_tok):
                    case ('label', val):
                        label_name = val[:-1].decode()
                        if label_name in namespace:
                            raise NameConflictError(
                                f'Label {label_name!r} cannot be redefined',
                                scan.get_origin()
                            )

                        namespace[label_name] = expr.Label(
                            scan.get_origin(), label_name,
                            self.sections[section], len(self.sections[section])
                        )
                        continue

                    case ('preproc', _):
                        match scan.read(ident_pat):
                            case b'section':
                                expect_space(scan)
                                section = self.read_section(scan)
                                self.prepare_section(section)
                            case b'format':
                                expect_space(scan)
                                item, setting = self.read_format_spec(scan)
                                if self.format.setdefault(item, setting) != setting:
                                    raise AssemblerError(
                                        f'The {item} format was previously set to {self.format[item]}, '
                                        f'which conflicts with the value {setting}',
                                        scan.get_origin()
                                    )
                            case None:
                                raise AssemblerSyntaxError.unhelpful(scan.get_origin())
                            case bad_command:
                                raise AssemblerSyntaxError(
                                    f'No such preprocessor command {bad_command.decode()!r}',
                                    scan.get_origin()
                                )

                        if not is_end(scan):
                            raise AssemblerSyntaxError.unhelpful(scan.get_origin())
                break


            if is_end(scan):
                continue


            if section == 'code':
                directive = read_instruction(scan, namespace, self.mf)
            else:
                directive = read_data_direc(scan, namespace, self.mf)

            self.sections[section].append(directive)
