import textwrap
from spasm.parser import Parser as SphinxParser
from spasm.context import ExecutionContext, VirtualContext
from spasm.emulator import Emulator

class RecorderContext(ExecutionContext):
    def __init__(self):
        super().__init__()
        self.reset()
        self.vctx = VirtualContext()

    def reset(self):
        self.flags = []
        self.bytes = bytearray()
        self.time_slept = 0

    def output(self, val):
        self.bytes += val[:1]

    def sleep(self, millis):
        self.time_slept += millis

    def on_flag(self, prog, flag):
        self.flags.append(flag)

    def virtualize(self):
        return self.vctx


def make_emulator(src, args=()):
    ps = SphinxParser(args)
    ps.parse_lines(textwrap.dedent(src).strip('\n').encode('utf-8').split(b'\n'))
    return Emulator(
        ps.get_program(),
        ctx=RecorderContext()
    )


def run_to_flag(emulator, expected_flag=None, *, max_cycles=100000):
    initial_flags = len(emulator.ctx.flags)
    for _ in range(max_cycles):
        if len(emulator.ctx.flags) != initial_flags:
            if expected_flag is not None:
                flag = emulator.ctx.flags[initial_flags]
                assert flag == expected_flag, f'unexpected flag {flag}'
            return bytes(emulator.ctx.bytes)
        if not emulator.step():
            assert False, 'program halted'
    assert False, 'max cycles exceeded'


def test_count():
    emulator = make_emulator("""
        %argv <count>
        %section state
        counter: .arg count word
        %section code
        loop:
            yield [counter]
            sub [counter], [counter], 1
        j loop
        hge [counter], 0

        flag done
        tnt: j tnt
        halt
    """, ['3'])

    assert list(run_to_flag(emulator, 'done')) == [3, 2, 1, 0]
