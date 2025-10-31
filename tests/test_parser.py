import textwrap
import math
import sys

import pytest
from pytest import raises

from spasm.errors import *
from spasm.parser import Parser as SphinxParser
from spasm.context import output_map


def parse(src, *, args=(), raw=False):
    if not raw:
        src = textwrap.dedent(src).strip('\n')
    lines = src.encode('utf-8').split(b'\n')

    ps = SphinxParser(args)
    ps.parse_lines(lines)
    return ps

def make_program(src, **kwargs):
    return parse(src, **kwargs).get_program()


@pytest.mark.parametrize("src, word_size, output_format", [
    ("", 2, 'signed'),
    ("%format word 3", 3, 'signed'),
    ("%format word 0x100", 0x100, 'signed'),
    # character literals are very silly to use here, but are allowed
    (r"%format word '\x01'", 1, 'signed'),
    ("%format output byte", 2, 'byte'),
    ("%format output signed", 2, 'signed'),
    ("%format output unsigned", 2, 'unsigned'),
    ("%format word 3\n%format output byte", 3, 'byte')
])
def test_formats(src, word_size, output_format):
    ps = parse(src)
    prog = ps.get_program()
    ctx = ps.get_output_context()
    assert prog.mf.word_size == word_size
    # Contexts don't have __eq__, so just check type for now
    assert type(ctx) is type(output_map[output_format]())


@pytest.mark.parametrize("src, err_match", [
    ("%format output potato", 'Invalid output format'),
    ("%format output BYTE", 'Invalid output format'),
    ("%format output bytes", 'Invalid output format'),
    ("%format output", None), ("%format output ", None),
    ("%format word -1", 'must be positive integer or inf'),
    ("%format word 0", 'must be positive integer or inf'),
    ("%format word 1+1", None),  # no math allowed (different error msg)
    ("%section state\n.zero 1\npotato:\n%format word potato",
     'must be positive integer or inf'),
    ("%format word", None), ("%format word ", None),
    ("%format potato", 'Invalid format specifier'),
    ("%format word1", 'Invalid format specifier'),
    ("%format wordle 6", 'Invalid format specifier'),
    ("%format", None), ("%format ", None)
])
def test_format_errors(src, err_match):
    with raises(AssemblerSyntaxError, match=err_match):
        make_program(src)


def test_format_conflict():
    with raises(AssemblerError, match='word format .* conflict'):
        make_program("""
            %format word 2
            %format word 3
        """)

    with raises(AssemblerError, match='output format .* conflict'):
        make_program("""
            %format output byte
            %format output unsigned
        """)


@pytest.mark.skipif(not math.isfinite(sys.maxsize), reason='Turing complete')
def test_missing_integers_for_inf_word_size():
    with raises(OSError, match='Your system lacks some of the integers'):
        make_program("%format word inf")


def test_cyclic_labels():
    assert make_program("""
        %format word 2
        %section state
        .word end - begin  ; 2 bytes
        begin:
        .ascii "Hello"     ; 5 bytes
        .byte 0            ; 1 byte
        .word 0            ; 2 bytes
        .zero 2 * begin    ; begin = 2, so 4 bytes
        .fill end, begin   ; begin = 2, so 2 bytes
        end:
    """).state[0] == 5 + 1 + 2 + 4 + 2

    with raises(LabelError, match='did not have a concrete address'):
        # Here the after label is defined, but has a cyclic dependency
        # which cannot be resolved.
        make_program("""
            %format word 2
            %section state
            .zero after
            after:
        """)

    with raises(ExpressionError, match='not defined in this namespace'):
        # The potato label is not defined at all.
        make_program("""
            %format word 2
            %section state
            .zero potato
            after:
        """)


def test_label_sections():
    prog = make_program("""
        %format word 2
        %section state
        .word label_state
        .zero 5
        label_state:
        
        %section const
        .word label_const
        .zero 10
        label_const:
    """)
    assert prog.state[0] == 2 + 5
    assert prog.const[0] == 2 + 10

    with raises(NameConflictError, match='cannot be redefined'):
        make_program("""
            %format word 2
            %section state
            .word label
            .zero 5
            label:
            
            %section const
            .word label
            .zero 10
            label:
        """)


def test_repeated_data_sections():
    prog = make_program("""
        %format word 2
        %section state
        .word end_state - start_state
        start_state:
        .ascii "state: "
        %section const
        .word end_const - start_const
        start_const:
        .ascii "const: "
        %section state
        .ascii "mutable"
        end_state:
        %section const
        .ascii "immutable"
        end_const:
    """)

    assert bytes(prog.state[2:]) == b'state: mutable'
    assert prog.state[0] == len(b'state: mutable')
    assert bytes(prog.const[2:]) == b'const: immutable'
    assert prog.const[0] == len(b'const: immutable')
    assert prog.state[1] == prog.const[1] == 0


@pytest.mark.parametrize("expr, expected", [
    ("10", 10), ("1_234", 1_234), ("1_1", 1_1), ("010", 10),
    ("0x10", 0x10), ("0x12_ab_CD_ef", 0x12_ab_CD_ef),
    ("0o10", 0o10), ("0o1_234_567", 0o1_234_567),
    ("0b10", 0b10), ("0b1010_1111", 0b1010_1111),
    (r"'A'", ord('A')), (r"'\n'", ord('\n')),
    (r"'\''", ord("'")), ('\'"\'', ord('"')), ('\'\\"\'', ord('"')),
    ("_1000\n_1000:", 4) # label
])
def test_numeric_literal(expr, expected):
    assert make_program(f"""
        %format word 4
        %section state
        .word {expr}
    """).signed(('sv', 0)) == expected


@pytest.mark.parametrize("expr", [
    "0Xff", "0xg", "0O7", "0o8", "0B1", "0b2",
    "1__1", "0x_10", "0x1__1", "0o_10", "0o1__1", "0b_10", "0b1__1",
    "1_", "0x1_", "0o1_", "0b1_"
])
def test_bad_numeric_literal(expr):
    with raises(AssemblerSyntaxError):
        make_program(f"""
            %format word 4
            %section state
            .word {expr}
        """)


@pytest.mark.parametrize("comment", ["", " ; comment"])
@pytest.mark.parametrize("expr, expected", [
    ("2+2", 2+2),
    ("2+3*4", 2+3*4),
    ("2*3+4", 2*3+4),
    ("(2+3)*4", (2+3)*4),
    ("-(2+3)", -(2+3)),
    ("(((((1)))))", 1),
    ("--1", --1),
    ("~-+-~+5", ~-+-~+5),
    ("2--1", 2--1),
    ("2/3", 2//3),
    ("-2/3", -2//3),
    ("16/4/2", 16//4//2),
    ("4/2*3/2", 4//2*3//2),
    # Sphinx does not follow C convention for bitwise op order
    ("1<<4-1", (1<<4)-1),
    ("1+2&2", 1+(2&2)),
    ("1<<2|1<<3", 1<<2|1<<3),
    ("0b10 & 0b110 | 0b101 & 0b01", 0b10 & 0b110 | 0b101 & 0b01),
    ("('B' + 3) * 2", (ord('B') + 3) * 2)
])
def test_math(expr, expected, comment):
    assert make_program(f"""
        %format word 2
        %section state
        .word {expr}{comment}
    """).signed(('sv', 0)) == expected


@pytest.mark.parametrize("expr, error", [
    ("(()", AssemblerSyntaxError),
    ("())", AssemblerSyntaxError),
    ("(-)", AssemblerSyntaxError),
    ("2++", AssemblerSyntaxError),
    ("2+/", AssemblerSyntaxError),
    ("2 2", AssemblerSyntaxError),
    ("*3", AssemblerSyntaxError),
    (";1", AssemblerSyntaxError),
    ("", AssemblerSyntaxError),
    ("1/0", EvaluationError)
])
def test_bad_math(expr, error):
    with raises(error):
        make_program(f"""
            %format word 2
            %section state
            .word {expr}
        """)


def test_word_suffix():
    assert make_program("""
        %format word 3
        %section state
        .word 10w
    """).signed(('sv', 0)) == 30

    assert make_program("""
        %section state
        .word 10w
        %format word 3
    """).signed(('sv', 0)) == 30

    assert make_program("""
        %section state
        .word 10w
    """).signed(('sv', 0)) == 20


@pytest.mark.parametrize("comment", ["", " ; comment"])
@pytest.mark.parametrize("directive, expected", [
    (".byte 0x42, 0x65, 0x6e",  b"Ben"),
    (".byte 0x42, 0x65, 0x6e,", b"Ben"),
    (".byte 0x42,", b"B"),
    (".word 1, 2, 3", b"\x01\x00\x02\x00\x03\x00")
])
def test_directive_multi_expr(directive, expected, comment):
    assert bytes(make_program(f"""
        %format word 2
        %section state
        {directive}{comment}
    """).state) == expected


@pytest.mark.parametrize("directive", [
    ".byte",
    ".byte ; comment",
    ".byte 0x42, 0x65, 0x6e,,",
    ".byte 0x42, , 0x65, 0x6e",
    ".byte ,0x42",
    ".byte ,"
])
def test_bad_multi_expr(directive):
    with raises(AssemblerSyntaxError):
        bytes(make_program(f"""
            %format word 2
            %section state
            {directive}
        """).state)


@pytest.mark.parametrize("count", [0, 1, 100])
@pytest.mark.parametrize("directive_fmt, fill_byte", [
    (".zero {count}", b'\0'),
    (".fill 0, {count}", b'\0'),
    (".fill 'B', {count}", b'B'),
])
def test_fill(count, directive_fmt, fill_byte):
    assert bytes(make_program(f"""
        %format word 2
        %section state
        {directive_fmt.format(count=count)}
    """).state) == fill_byte * count

@pytest.mark.parametrize("directive, error, err_match", [
    (".zero -1", ExpressionError, 'must not be negative'),
    (".fill 0, -1", ExpressionError, 'must not be negative'),
    (".zero 0, 0", AssemblerSyntaxError, 'Too many arguments'),
    (".fill 0, 0, 0", AssemblerSyntaxError, 'Too many arguments'),
    (".fill 0, 0,", AssemblerSyntaxError, 'Too many arguments'),
    (".fill 0,", AssemblerSyntaxError, 'found end of argument list'),
    (".fill 0", AssemblerSyntaxError, 'found end of argument list'),
    (".fill -1, 0", ValueError, 'must be in range'),
    (".fill -1, 1", ValueError, 'must be in range'),
    (".fill 256, 0", ValueError, 'must be in range'),
    (".fill 256, 1", ValueError, 'must be in range')
])
def test_bad_fill(directive, error, err_match):
    with raises(error, match=err_match):
        bytes(make_program(f"""
            %format word 2
            %section state
            {directive}
        """).state)


@pytest.mark.parametrize("directive, convert", [
    (".ascii", lambda s: s),
    (".asciiz", lambda s: s + b'\0'),
    (".asciip", lambda s: len(s).to_bytes(3, 'little') + s)
])
@pytest.mark.parametrize("string, expected", [
    (r"", b''),
    (r"Hello, world!", b'Hello, world!'),
    (r"💩", '💩'.encode('utf-8')),
    (r'\"', b'"'),
    (r"'\'", b"''"),
    (r";", b';'),
    (r"[\0]", b'[\0]'),
    (r"\a\b\f\n\r\t\0\\", b'\a\b\f\n\r\t\0\\')
])
def test_ascii_directives(directive, convert, string, expected):
    assert bytes(make_program(f"""
        %section state
        {directive} "{string}"
        %format word 3
    """).state) == convert(expected)


@pytest.mark.parametrize("directive, error, err_match", [
    (r".ascii 'B'", AssemblerSyntaxError, 'Expected string literal'),
    (r'.byte "B"', AssemblerSyntaxError, 'Expected expression'),
    (r'.ascii "hello', AssemblerSyntaxError, 'Unterminated string literal'),
    (r'.ascii "hello", "world"', AssemblerSyntaxError, 'Too many arguments'),
    (r'.ascii "hello" "world"', AssemblerSyntaxError, None),
    (r'.ascii "\?"', AssemblerSyntaxError, 'Invalid escape sequence'),
    (r'.ascii"hello"', AssemblerSyntaxError, 'Expected space')
])
def test_bad_ascii_directives(directive, error, err_match):
    with raises(error, match=err_match):
        bytes(make_program(f"""
            %section state
            {directive}
        """).state)
