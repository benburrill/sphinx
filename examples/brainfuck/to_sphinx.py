def gen_data(input_str, data_size):
    escaped = input_str.translate(str.maketrans({
        '\\': '\\\\',
        '"': '\\"',
        '\n': '\\n'
    }))

    yield '%section const'
    yield f'input: .asciiz "{escaped}"'

    yield '%section state'
    yield 'value: .word 0'
    yield 'ip: .word input'
    yield 'dp: .word data'
    yield f'data: .zero {data_size}'


def gen_code(brainfuck):
    depth = 0
    count = {}
    for c in brainfuck:
        if c == '>':
            yield 'add [dp], [dp], 1'
        elif c == '<':
            yield 'sub [dp], [dp], 1'
        elif c == '+':
            yield 'lbs [value], [dp]'
            yield 'add [value], [value], 1'
            yield 'sbs [dp], [value]'
        elif c == '-':
            yield 'lbs [value], [dp]'
            yield 'sub [value], [value], 1'
            yield 'sbs [dp], [value]'
        elif c == '.':
            yield 'lbs [value], [dp]'
            yield 'yield [value]'
        elif c == ',':
            yield 'lbc [value], [ip]'
            yield 'sbs [dp], [value]'
            yield 'add [ip], [ip], 1'
        elif c == '[':
            count[depth] = count.setdefault(depth, 0) + 1
            yield f'j end_bracket_{depth}_{count[depth]}'
            yield f'begin_bracket_{depth}_{count[depth]}:'
            yield 'lbs [value], [dp]'
            yield 'heq [value], 0'
            depth += 1
        elif c == ']':
            depth -= 1
            yield f'j begin_bracket_{depth}_{count[depth]}'
            yield f'end_bracket_{depth}_{count[depth]}:'
            yield 'lbs [value], [dp]'
            yield 'hne [value], 0'


def runner(brainfuck, input_str, data_size):
    yield from gen_data(input_str, data_size)

    yield '%section code'
    yield from gen_code(brainfuck)
    yield 'flag done'
    yield 'tnt: j tnt'
    yield 'halt'


def forecaster(brainfuck, input_str, data_size):
    yield from gen_data(input_str, data_size)

    yield '%section code'
    yield 'j will_halt'
    yield 'flag will_not_halt'
    yield 'flag done'
    for line in gen_code(brainfuck):
        if not line.startswith('yield'):
            yield line
    yield 'halt'
    yield 'will_halt: flag will_halt'
    yield 'flag done'
    yield 'tnt: j tnt'
    yield 'halt'


if __name__ == '__main__':
    import sys
    args = iter(sys.argv[1:])
    func = {'forecaster': forecaster, 'runner': runner}[next(args)]
    with open(next(args)) as file:
        for line in func(file.read(), next(args, ''), int(next(args, '1000'))):
            print(line)
