from abc import ABC, abstractmethod
import time
import sys

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
    def sleep(self, millis):
        pass

    @abstractmethod
    def on_flag(self, prog, flag):
        pass

    @abstractmethod
    def virtualize(self):
        pass

    # @abstractmethod
    # def run_syscall(self, syscall):
    #     pass


class VirtualContext(ExecutionContext):
    def output(self, val):
        pass

    def sleep(self, millis):
        pass

    def on_flag(self, prog, flag):
        pass

    def virtualize(self):
        return self


class RealContext(ExecutionContext):
    def __init__(self, *, vctx=None):
        super().__init__()
        self.vctx = vctx if vctx is not None else VirtualContext()
        self.last_progress = None

    def virtualize(self):
        return self.vctx

    def sleep(self, millis):
        time.sleep(millis / 1000)

    def on_flag(self, prog, flag):
        print(f'Reached {flag} flag', file=sys.stderr)
        match flag:
            case 'done' | 'error' | 'win' | 'lose':
                print(f'    CPU time: {self.total_time} clock cycles', file=sys.stderr)
                emulation_time = self.vctx.total_time + self.total_time
                print(f'    Emulator efficiency: {self.total_time / emulation_time:.2%}', file=sys.stderr)
            case 'progress':
                message = f'    CPU time: {self.total_time} clock cycles'
                if self.last_progress is not None:
                    message += f' ({self.total_time - self.last_progress} since last progress)'
                self.last_progress = self.total_time
                print(message, file=sys.stderr)
            case 'debug':
                print(f'    PC: {prog.pc}', file=sys.stderr)
                print(f'    State: {prog.state.hex(" ", -prog.mf.word_size)}', file=sys.stderr)


class IntOutputContext(RealContext):
    def __init__(self, *, signed, vctx=None):
        super().__init__(vctx=vctx)
        self.signed = signed

    def output(self, word):
        print(int.from_bytes(word, 'little', signed=self.signed))


class ByteOutputContext(RealContext):
    def __init__(self, *, vctx=None):
        super().__init__(vctx=vctx)
        self.last_byte = b'\n'

    def on_flag(self, prog, flag):
        if self.last_byte != b'\n':
            sys.stdout.flush()
            print(file=sys.stderr)
            self.last_byte = b'\n'

        super().on_flag(prog, flag)

    def output(self, word):
        low_byte = bytes(word[:1])
        sys.stdout.buffer.write(low_byte)
        self.last_byte = low_byte

        # sys.stdout.buffer isn't line buffered, even if sys.stdout is
        if low_byte == b'\n' and sys.stdout.line_buffering:
            sys.stdout.flush()


output_map = {
    'byte': ByteOutputContext,
    'signed': lambda: IntOutputContext(signed=True),
    'unsigned': lambda: IntOutputContext(signed=False)
}
