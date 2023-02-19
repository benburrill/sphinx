from abc import ABC, abstractmethod
from parser import Parser

from errors import *


class Emulator:
    def __init__(self, prog, vctx=None, rctx=None, cycle=None):
        self.prog = prog
        self.cycle = cycle

        self.vctx = vctx if vctx is not None else VirtualContext()
        self.rctx = rctx if rctx is not None else RealContext()

    @classmethod
    def run_from_file(cls, fname, reraise=False):
        ps = Parser()

        try:
            ps.parse_file(fname)
            prog = ps.get_program()
        except AssemblerError as err:
            ps.handle_error(err)
            if reraise:
                raise
            return

        cls(prog).run()

    def step(self):
        match self.prog.exec(self.rctx):
            case (new_pc,):
                self.prog.pc = new_pc
            case (pc_cont, pc_jump):
                if self.cycle:
                    if self.cycle.do_jump:
                        self.prog.pc = pc_jump
                    else:
                        self.prog.pc = pc_cont
                    self.cycle = self.cycle.tail
                else:
                    self.cycle = self.prog.jump(pc_cont).find_cycle(self.vctx)
                    if self.cycle is None:
                        self.prog.pc = pc_jump
                    else:
                        self.prog.pc = pc_cont
            case ():
                return False
        return True

    def run(self):
        # Possibly I should add a mechanism for contexts or something to
        # request that execution be paused, returning early from run.
        while self.step():
            pass


class ExecutionContext(ABC):
    def __init__(self):
        self.total_time = 0

    # Called right before any instruction is executed.
    def before_exec(self, prog):
        self.total_time += 1

    @abstractmethod
    def output(self, val):
        pass

    @abstractmethod
    def on_flag(self, prog, flag):
        pass

    # @abstractmethod
    # def run_syscall(self, syscall):
    #     pass


class VirtualContext(ExecutionContext):
    def output(self, val):
        pass

    def on_flag(self, prog, flag):
        pass


class RealContext(ExecutionContext):
    def output(self, val):
        print(val)

    def on_flag(self, prog, flag):
        print(f'Reached {flag} flag')
        match flag:
            case 'done' | 'error' | 'win' | 'lose':
                print(f'    Time taken: {self.total_time} cycles')
            case 'debug':
                print(f'    PC: {prog.pc}')
                print(f'    State: {prog.state.hex(" ", -prog.mf.word_size)}')


if __name__ == '__main__':
    import sys
    Emulator.run_from_file(sys.argv[1], reraise=False)
