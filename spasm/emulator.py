from .parser import Parser
from .context import VirtualContext, IntOutputContext

from .errors import *


class Emulator:
    def __init__(self, prog, vctx=None, rctx=None, cycle=None):
        self.prog = prog
        self.cycle = cycle

        self.vctx = vctx if vctx is not None else VirtualContext()
        self.rctx = rctx if rctx is not None else IntOutputContext(signed=True)
        self.rctx.on_done = self.show_stats

    def show_stats(self):
        print(f'    CPU time: {self.rctx.total_time} clock cycles')
        emulation_time = self.vctx.total_time + self.rctx.total_time
        print(f'    Emulator efficiency: {self.rctx.total_time / emulation_time:.2%}')

    @classmethod
    def run_from_file(cls, fname, reraise=False):
        ps = Parser()

        try:
            ps.parse_file(fname)
            prog = ps.get_program()
            rctx = ps.get_output_context()
        except AssemblerError as err:
            ps.handle_error(err)
            if reraise:
                raise
            return

        cls(prog, rctx=rctx).run()

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
                assert self.cycle is None
                return False
        return True

    def run(self):
        # Possibly I should add a mechanism for contexts or something to
        # request that execution be paused, returning early from run.
        while self.step():
            pass
