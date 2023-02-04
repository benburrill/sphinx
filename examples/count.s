; Just counts upwards to 10.  No magic.

%format word 2
%section state
counter: .word 0

%section code
loop:
    yield [counter]
    add [counter], [counter], 1
    j loop
    hlt [counter], 10
flag done
tnt: j tnt
halt
