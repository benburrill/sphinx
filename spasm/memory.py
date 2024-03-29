import math
import sys


def signed_bytes_needed(num):
    # Number of bytes needed to store the signed value num
    if num < 0:
        num += 1

    return -((num.bit_length() + 1) // -8)


class MemoryFormat:
    def __init__(self, word_size):
        self.set_word_size(word_size)

    def set_word_size(self, word_size):
        if word_size == 'inf':
            if math.isfinite(sys.maxsize):
                raise OSError(
                    'Your system lacks some of the integers necessary '
                    'to support the infinite word size'
                )
            else:
                raise NotImplementedError('Nice try')
        else:
            self.word_mask = (1 << (8 * word_size)) - 1
            self.word_size = word_size

    def __repr__(self):
        return f'<{self.word_size * 8} bit words>'

    def read_word(self, buf, addr):
        end = addr + self.word_size
        if addr < 0 or end > len(buf):
            raise IndexError(f'Read error: no word at address {addr}')

        return buf[addr:end]

    def write_word(self, buf, addr, word):
        end = addr + self.word_size
        if addr < 0 or end > len(buf):
            raise IndexError(f'Write error: no word at address {addr}')

        buf[addr:end] = word

    def read_byte(self, buf, addr):
        if addr < 0 or addr >= len(buf):
            raise IndexError(f'Read error: no byte at address {addr}')

        return buf[addr]

    def write_byte(self, buf, addr, byte):
        if addr < 0 or addr >= len(buf):
            raise IndexError(f'Write error: no byte at address {addr}')

        buf[addr] = byte & 0xFF

    def int_bytes(self, val):
        return (val & self.word_mask).to_bytes(self.word_size, 'little')

    def write_int(self, buf, addr, val):
        return self.write_word(buf, addr, self.int_bytes(val))

    def array_from_words(self, words):
        array = bytearray(self.word_size * len(words))
        addr = 0
        for val in words:
            self.write_int(array, addr, val)
            addr += self.word_size
        return array

    def __copy__(self):
        return MemoryFormat(self.word_size)

    def copy(self):
        return self.__copy__()

    def is_safe_unsigned(self, num):
        return 0 <= num <= self.word_mask

    def is_safe_signed(self, num):
        return signed_bytes_needed(num) <= self.word_size
