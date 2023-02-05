; Demonstrates loops that take a long time to repeat a state

%format word 3
%section state
counter: .word 0

%section code
; This initial jump, if uncommented, forces the emulator to determine
; whether the loop will lead to a halt, which takes a large amount of
; memory and time for a word size of 3 bytes (about 2.3 GB and over 3
; minutes on my machine) before it can start running.
; j somewhere

loop:
    ; Putting the jump inside the loop makes it worse, requiring 3.3 GB
    ; j somewhere
    yield [counter]
    add [counter], [counter], 1
j loop
halt

somewhere:
