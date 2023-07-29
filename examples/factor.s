; If the number is prime, it is indicated as such immediately.
; If the number is composite, it is factored into two numbers != 1 with
; a worst-case time complexity of O(log(N))
; A very similar algorithm is used recursively in this HiD program:
; https://github.com/benburrill/halt_is_defeat/blob/main/examples/factor.hid
; to produce a complete prime factorization, but that is not done here.

%format word 2
%section const
; Good test cases: 437 = 19*23, 439 = 1*439
; NOTE: This program is not valid for numbers less than 2, which will be
; incorrectly reported as prime.
number:
%argv [<number>]
.arg number word
.word 439 ; Default

%section state
factor: .word 0
bit: .word 1
temp: .word 0

%section code
j prime
flag will_be_composite
asr [temp], {number}, 1
loop:
    hgt [bit], [temp]
    j continue
    add [factor], [factor], [bit]
    continue:
    asl [bit], [bit], 1
j loop
hle [factor], 1
mod [temp], {number}, [factor]
hne [temp], 0

flag composite
yield [factor]
div [factor], {number}, [factor]
yield [factor]
j done
halt

prime:
flag prime
yield {number}
done: flag done
tnt: j tnt
halt
