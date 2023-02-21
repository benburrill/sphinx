; Just counts down from 10.  No magic.

%format word 2
%section state
counter: .word 10

%section code
loop:
    yield [counter]
    sub [counter], [counter], 1
j loop
hgt [counter], 0

; Blast-off!  Signal program success and enter infinite loop
flag done
tnt: j tnt
halt
