; This prints a decimal expansion of a fraction, with repeating portion
; in parentheses, without any redundant digits.
; It demonstrates the use of the byte output format.

; TODO: explain, simplify, and test this better

%format output byte
; 32 bit words -- terrifying!
; Probably you could use TBs of RAM finding the reciprocals of very
; large "full reptend" primes, but I've yet to find any fractions that
; cause any issues.
%format word 4

%section state
; 84823/27000 is a pretty inefficient rational approximation of pi,
; specifically designed so that the repeating portion occurs after a
; non-repeating part.
num: .word 84823
den: .word 27000

; Known bugs:
; * Large-ish numbers on small word size can result in digits being
;   printed in infinite loop.

top: .word 0
addr: .word int_buf
temp: .word 0

; 3 words is enough to store the base-10 digits of a word as bytes
; We then reuse the buffer later for checking for repeating fractions
int_buf:
prev_num: .word 0
fast: .word 0
stop: .word 0

%section const
digits: .ascii "0123456789"

%section code
; Just halt right away if denominator is 0
; TODO: maybe handle better
heq [den], 0

j den_pos
hge [den], 0
mul [num], [num], -1
mul [den], [den], -1
den_pos:

j num_pos
hge [num], 0
mul [num], [num], -1
yield '-'
num_pos:

div [top], [num], [den]
mod [num], [num], [den]

get_int_digits:
    mod [temp], [top], 10
    div [top], [top], 10

    lbco [temp], digits, [temp]
    sbs [addr], [temp]
    add [addr], [addr], 1
j get_int_digits
hne [top], 0

print_int_digits:
    sub [addr], [addr], 1
    lbs [temp], [addr]
    yield [temp]
j print_int_digits
hgt [addr], int_buf

mov [stop], 0
j done
heq [num], 0
yield '.'

mov [prev_num], [num]
mov [fast], [num]

wrong_loop:
hne [stop], 0
hne [fast], [prev_num]

mov [fast], [num]
mov [prev_num], [num]

j lookahead
mov [stop], [num]
yield '('
lookahead:
    mul [num], [num], 10
    div [top], [num], [den]
    mod [num], [num], [den]
    lbco [temp], digits, [top]
    yield [temp]

    j wrong_loop

    j done
    heq [num], [stop]

    mul [fast], [fast], 100
    mod [fast], [fast], [den]
    heq [num], [fast]
j lookahead
halt


done:
hne [num], [stop]
j end_zero
heq [stop], 0
yield ')'
end_zero:
yield '\n'

flag done
tnt: j tnt
halt
