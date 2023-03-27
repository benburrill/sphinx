from dataclasses import dataclass
from collections import deque
from collections.abc import Sequence
from .memory import MemoryFormat, signed_bytes_needed
import enum


@dataclass
class CodeTable(Sequence):
    instr: tuple

    def __str__(self):
        # Convert code table back into readable instructions
        # Ideally the result should be valid syntax, though I think it
        # won't quite be how I'm doing it currently sadly.
        result = ""
        for name, *args in self.instr:
            result += f'{name} {", ".join(map(self._arg_str, args))}\n'

        return result

    def _arg_str(self, arg):
        match arg:
            case ('im', val):
                return str(val)
            case ('sv', val):
                return f'[{val}]'
            case ('cv', val):
                return f'{{{val}}}'
            case _:
                return str(arg)

    def __getitem__(self, addr):
        # Probably when we add syscalls, CodeTable will hold a syscall
        # table as well and negative addresses will be mapped to some
        # pseudo-instruction, eg ('%syscall%', syscall_func) -- actually
        # executing the syscall (ie just calling it) would still be
        # Program's responsibility
        if addr < 0 or addr >= len(self.instr):
            return ('halt',)

        return self.instr[addr]

    # Defining an unbounded __getitem__ kinda "forces" us to make it
    # properly iterable because otherwise Python will make it iterable,
    # but badly.  Even when using Sequence with __len__, it still makes
    # it be an infinite iterable, which is not what I want.
    def __len__(self):
        return len(self.instr)

    def __iter__(self):
        return iter(self.instr)



@dataclass
class Program:
    mf: MemoryFormat
    code: CodeTable
    state: memoryview
    const: bytes
    pc: int = 0

    def exec(self, ctx):
        # Execute current instruction, returning possible subsequent pc

        ctx.before_exec(self)
        match self.code[self.pc]:
            case ('j', varg):
                return (self.pc + 1, self.signed(varg))
            case ('halt',):
                return ()
            case ('hlt', vleft, vright):
                if self.signed(vleft) < self.signed(vright):
                    return ()
            case ('hgt', vleft, vright):
                if self.signed(vleft) > self.signed(vright):
                    return ()
            case ('hle', vleft, vright):
                if self.signed(vleft) <= self.signed(vright):
                    return ()
            case ('hge', vleft, vright):
                if self.signed(vleft) >= self.signed(vright):
                    return ()
            case ('heq', vleft, vright):
                if self.signed(vleft) == self.signed(vright):
                    return ()
            case ('hne', vleft, vright):
                if self.signed(vleft) != self.signed(vright):
                    return ()
            case ('yield', varg):
                ctx.output(self.bytes(varg))
            case ('sleep', varg):
                ctx.sleep(self.unsigned(varg))
            case ('add', out, vleft, vright):
                self.mf.write_int(self.state, out, self.signed(vleft) + self.signed(vright))
            case ('sub', out, vleft, vright):
                self.mf.write_int(self.state, out, self.signed(vleft) - self.signed(vright))
            case ('mul', out, vleft, vright):
                self.mf.write_int(self.state, out, self.signed(vleft) * self.signed(vright))
            case ('div', out, vleft, vright):
                try: self.mf.write_int(self.state, out, self.signed(vleft) // self.signed(vright))
                except ZeroDivisionError: pass
            case ('mod', out, vleft, vright):
                try: self.mf.write_int(self.state, out, self.signed(vleft) % self.signed(vright))
                except ZeroDivisionError: pass
            case ('and', out, vleft, vright):
                self.mf.write_int(self.state, out, self.signed(vleft) & self.signed(vright))
            case ('or', out, vleft, vright):
                self.mf.write_int(self.state, out, self.signed(vleft) | self.signed(vright))
            case ('xor', out, vleft, vright):
                self.mf.write_int(self.state, out, self.signed(vleft) ^ self.signed(vright))
            case ('asl', out, vleft, vright):
                shift_count = self.signed(vright) % (self.mf.word_size * 8 + 1)
                self.mf.write_int(self.state, out, self.signed(vleft) << shift_count)
            case ('asr', out, vleft, vright):
                shift_count = self.signed(vright) % (self.mf.word_size * 8 + 1)
                self.mf.write_int(self.state, out, self.signed(vleft) >> shift_count)
            case ('mov', out, varg):
                self.mf.write_word(self.state, out, self.bytes(varg))
            case ('lws', out, vsa):
                self.mf.write_word(
                    self.state, out,
                    self.mf.read_word(self.state, self.unsigned(vsa))
                )
            case ('lbs', out, vsa):
                self.mf.write_int(
                    self.state, out,
                    self.mf.read_byte(self.state, self.unsigned(vsa))
                )
            case ('lwso', out, vsa, voff):
                self.mf.write_word(
                    self.state, out,
                    self.mf.read_word(self.state, self.unsigned(vsa) + self.signed(voff))
                )
            case ('lbso', out, vsa, voff):
                self.mf.write_int(
                    self.state, out,
                    self.mf.read_byte(self.state, self.unsigned(vsa) + self.signed(voff))
                )
            case ('lwc', out, vca):
                self.mf.write_word(
                    self.state, out,
                    self.mf.read_word(self.const, self.unsigned(vca))
                )
            case ('lbc', out, vca):
                self.mf.write_int(
                    self.state, out,
                    self.mf.read_byte(self.const, self.unsigned(vca))
                )
            case ('lwco', out, vca, voff):
                self.mf.write_word(
                    self.state, out,
                    self.mf.read_word(self.const, self.unsigned(vca) + self.signed(voff))
                )
            case ('lbco', out, vca, voff):
                self.mf.write_int(
                    self.state, out,
                    self.mf.read_byte(self.const, self.unsigned(vca) + self.signed(voff))
                )
            case ('sws', vsa, varg):
                self.mf.write_int(
                    self.state, self.unsigned(vsa),
                    self.signed(varg)
                )
            case ('sbs', vsa, varg):
                self.mf.write_byte(
                    self.state, self.unsigned(vsa),
                    self.signed(varg)
                )
            case ('swso', vsa, voff, varg):
                self.mf.write_int(
                    self.state, self.unsigned(vsa) + self.signed(voff),
                    self.signed(varg)
                )
            case ('sbso', vsa, voff, varg):
                self.mf.write_byte(
                    self.state, self.unsigned(vsa) + self.signed(voff),
                    self.signed(varg)
                )
            case ('flag', flag):
                ctx.on_flag(self, flag)
            case unimpl:
                raise NotImplementedError(f'Unimplemented instruction {unimpl}')

        return (self.pc + 1,)

    def read_spec(self, spec, signed=True, *, as_bytes):
        # Note: Unless as_bytes is set to True, immediate values will be
        # returned as-is, which means they may be larger than can fit in
        # a word, and signed has no effect on them.
        # If word-wrapped immediate values are needed, the simplest way
        # to get them is to set as_bytes to True.  The result can then
        # be treated as signed or unsigned as desired.
        match spec:
            case ('im', immediate):
                if as_bytes:
                    return self.mf.int_bytes(immediate)
                return immediate
            case ('cv', addr):
                word = self.mf.read_word(self.const, addr)
            case ('sv', addr):
                word = self.mf.read_word(self.state, addr)
            case _:
                raise ValueError(f'Invalid value specifier {spec}')

        if as_bytes:
            return word

        return int.from_bytes(word, 'little', signed=signed)

    def signed(self, spec):
        return self.read_spec(spec, signed=True, as_bytes=False)

    def unsigned(self, spec):
        return self.read_spec(spec, signed=False, as_bytes=False)

    def bytes(self, spec):
        return self.read_spec(spec, as_bytes=True)

    def run_until_branch(self, ctx):
        while True:
            options = self.exec(ctx)
            if len(options) != 1:
                return options

            self.pc, = options

    def save(self):
        # PC is signed because I plan to make use of negative addresses
        # in the future.
        pc_bytes = self.pc.to_bytes(
            signed_bytes_needed(self.pc),
            'little', signed=True
        )

        return pc_bytes + self.state

    def restore(self, sb):
        pc_size = len(sb) - len(self.state)
        self.pc = int.from_bytes(sb[:pc_size], 'little', signed=True)
        self.state[:] = sb[pc_size:]

    def fork(self):
        # Return new instance with copied state
        return Program(
            self.mf, state=memoryview(bytearray(self.state)),
            const=self.const, code=self.code, pc=self.pc
        )

    def jump(self, pc):
        # Unlike fork, jump does not create a copy of state
        # Instead it gives you kinda an alternative executor on the same
        # program where you have a second pc is wherever you want.
        # I'm not using it for anything fancy though, it's mostly just
        # convenient for stuff like prog.jump(somewhere).save() to set
        # the restore point to wherever you want without needing to
        # create more copies than necessary.
        return Program(
            self.mf, state=self.state, const=self.const,
            code=self.code, pc=pc
        )

    def find_cycle(self, ctx):
        # If a cycle is found from executing the program starting at pc,
        # return a cyclic linked list of booleans determining the future
        # jumps that will be taken, starting from pc on.
        # Otherwise return None.

        prog = self.fork()

        # path stores Jump decisions along the current path of execution
        # See the Jump enum
        path = deque()
        # history stores packed save states for all skipped jumps along
        # the path, including the address where taking a jump would have
        # lead if it were taken.
        history = deque()
        # breadcrumbs maps save states (as in history, after jump) to
        # CycleNode for all followed upward jumps along the path.
        breadcrumbs = {}

        decision = None

        while True:
            while True:
                options = prog.run_until_branch(ctx)
                if not options:
                    # Abandon timeline!
                    decision = None
                    break

                pc_cont, pc_jump = options
                sb = prog.jump(pc_jump).save()
                jump_info = Jump.SKIP

                # In checking for repeated states, the only ones that we
                # care about are those that lead to an upwards jump, as
                # any loop must have at least one upwards jump.
                if pc_jump < pc_cont:
                    jump_info |= Jump.UPWARD
                    try:  # Have we found a cycle?
                        decision = breadcrumbs[sb]
                        break
                    except KeyError: pass

                history.append(sb)
                path.append(jump_info)
                prog.pc = pc_cont

            while path:
                prev_jump = path.pop()
                if decision is not None:
                    # Time to unwind!
                    if Jump.FOLLOW not in prev_jump:
                        history.pop()
                        decision = CycleNode(False, decision)
                    elif Jump.UPWARD in prev_jump:
                        sb, prev_decision = breadcrumbs.popitem()
                        prev_decision.tail = decision
                        decision = prev_decision
                    else:
                        decision = CycleNode(True, decision)
                elif Jump.FOLLOW not in prev_jump:
                    # We can try taking another path
                    path.append(prev_jump | Jump.FOLLOW)
                    sb = history.pop()
                    if Jump.UPWARD in prev_jump:
                        breadcrumbs[sb] = CycleNode(True, None)
                    prog.restore(sb)
                    break
                elif Jump.UPWARD in prev_jump:
                    # There's nothing more that can be done, but we need
                    # to clean up the mess
                    breadcrumbs.popitem()
            else:
                # Stack is empty, we're done
                assert not history
                assert not breadcrumbs
                return decision



# Node in a cyclic linked list representing a path of execution which
# leads to a loop.
class CycleNode:
    __slots__ = 'do_jump', 'tail'
    def __init__(self, do_jump, tail):
        self.do_jump = do_jump
        self.tail = tail

    def __repr__(self):
        cur = self
        result = "("
        for i in range(1000):
            if cur is None:
                break
            result += "1" if cur.do_jump else "0"
            if i == 0: result += ")"
            cur = cur.tail
        result += "!" if cur is None else "..."

        return f'<CycleNode {result}>'


class Jump(enum.Flag):
    # SKIP and FOLLOW indicate whether a jump is taken or not, but do
    # not have the UPWARD flag set.
    SKIP = 0
    FOLLOW = enum.auto()
    # UPWARD should be set if taking the jump would move upwards in the
    # code, regardless of whether the jump was taken.
    UPWARD = enum.auto()
