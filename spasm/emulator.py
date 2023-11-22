from .parser import Parser
from .context import VirtualContext, IntOutputContext

from .errors import *


class Emulator:
    def __init__(self, prog, ctx=None, cycle=None):
        self.prog = prog
        self.cycle = cycle

        self.ctx = ctx if ctx is not None else IntOutputContext(signed=True)

    @classmethod
    def run_from_file(cls, fname, reraise=False, args=None):
        ps = Parser(args)

        try:
            ps.parse_file(fname)
            prog = ps.get_program()
            ctx = ps.get_output_context()
        except AssemblerError as err:
            ps.handle_error(err)
            if reraise:
                raise
            return 1

        cls(prog, ctx=ctx).run()
        return 0

    def step(self):
        match self.prog.exec(self.ctx):
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
                    self.cycle = self.prog.jump(pc_cont).find_cycle(self.ctx)
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
