; This prints a decimal expansion of a fraction, with repeating portion
; in parentheses, without any redundant digits.

; Repeating fractions are detected in a bit of an interesting way.  You
; can't avoid infinite loops in Sphinx the way you can halting, but what
; this program does is optimistically guess that a repetition will begin
; at each digit.  If the guess is correct, the loop will run until that
; state repeats and then breaks out to terminal non-termination.  If the
; guess would have been wrong, a slow cycle detector (tortoise and hare)
; is used to eventually halt the loop, but only AFTER we would have
; broken out if the guess was correct.  So we can use a jump instruction
; to test for that halt, and if would occur, we can guess that the next
; digit will be where the loop starts instead.
; In other words: it's the tortoise, the hare, and the time-traveler

; This program also demonstrates the use of the byte output format.

%format output byte

; 32 bit words -- terrifying!
; Some fractions, eg reciprocals of "full reptend" primes can use up a
; fair bit of memory, but it's less apocalyptic than you might imagine.
; Worst I've tried is 1/308927, but memory use stays under 150 MB.
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
; Just halt in case of 0 denominator
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
