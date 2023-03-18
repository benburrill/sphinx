from abc import ABC, abstractmethod
import contextlib
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


class RealContext(ExecutionContext):
    def __init__(self):
        super().__init__()
        self.on_done = lambda: None

    def sleep(self, millis):
        time.sleep(millis / 1000)

    def on_flag(self, prog, flag):
        with contextlib.redirect_stdout(sys.stderr):
            print(f'Reached {flag} flag')
            match flag:
                case 'done' | 'error' | 'win' | 'lose':
                    self.on_done()
                case 'debug':
                    print(f'    PC: {prog.pc}')
                    print(f'    State: {prog.state.hex(" ", -prog.mf.word_size)}')


class IntOutputContext(RealContext):
    def __init__(self, *, signed):
        super().__init__()
        self.signed = signed

    def output(self, word):
        print(int.from_bytes(word, 'little', signed=self.signed))


class ByteOutputContext(RealContext):
    def __init__(self):
        super().__init__()
        self.last_byte = b'\n'

    def on_flag(self, prog, flag):
        sys.stdout.flush()
        if self.last_byte != b'\n':
            print(file=sys.stderr)
            self.last_byte = b'\n'

        super().on_flag(prog, flag)

    def output(self, word):
        low_byte = word[:1]
        sys.stdout.buffer.write(low_byte)
        self.last_byte = bytes(low_byte)


output_map = {
    'byte': ByteOutputContext,
    'signed': lambda: IntOutputContext(signed=True),
    'unsigned': lambda: IntOutputContext(signed=False)
}
