; Demonstrates the byte output mode

%format output byte
%format word 2

%section const
message: .asciiz "Hello, world!\n"

%section state
char: .word 0
addr: .word message

%section code
loop:
    lbc [char], [addr]
    add [addr], [addr], 1
    ; Halt at end of string
    heq [char], 0
    yield [char]
j loop
halt
