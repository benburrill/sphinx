; Example of halt propagation for conditional branching

; Turing jumps combined with conditional halt instructions can be used
; to control conditional execution.
; For example, if we want to write if (x == y) { flag hi }, you could do
; | j after
; | hne [x], [y]
; |     flag hi
; | after:
; However, you might notice a problem.  `j after` cannot distinguish
; between a halt by the `hne [x], 1` and a later halt.  So if there is a
; later halt, the branch will get skipped, even if it should run.
;
; We can deal with this problem using halt propagation.  The idea is to
; propagate halts backwards through time by halting on complementary
; conditions in the branches of a conditional.
; So we would add add an else branch in which we heq [x], [y].
;
; This ensures that if a program should halt, that it will halt.
; If the program takes the wrong branch because it sees a future halt,
; it will halt early.
;
; You may still be concerned.  Although the halting behavior is correct,
; the output of the program might not be, because a halting program will
; halt earlier than was supposed to.
; In practice, this isn't a big deal.  All we need is to use terminal
; non-termination (an infinite loop) at the end of the program.
; Branches that don't reach TNT won't actually be run, so we don't care
; about the output that is produced, only that the halting behavior is
; correct (and halt propagation preserves halting behavior).
; Given that most Sphinx programs use TNT anyway for other reasons, this
; isn't much to ask.  So halt propagation is the canonical way to do
; conditional branching in Sphinx.

; If for whatever reason you want to branch without needing terminal
; non-termination, see branch_table.s

; -- Example --
; Consider the following program:
; | x = 1
; | y = 0
; | if (program will halt) {
; |     flag flip_x
; |     x = 1 - x
; | }
; | if (x == y) {
; |     flag flip_y
; |     y = 1 - y
; | }
; | flag after
; | if (y == 0) { halt }
; | flag done
; | while (true) { }

; Here's how we can write it with halt propagation:
%section state
x: .word 1
y: .word 0

%section code
j program_will_halt
j program_will_not_halt
halt
program_will_halt:
    flag flip_x
    sub [x], 1, [x]
program_will_not_halt:

j else
hne [x], [y]
    flag flip_y
    sub [y], 1, [y]
    j after   ; skip else branch
    halt
else:
heq [x], [y]  ; <-- halt propagation
after:

flag after

heq [y], 0

flag done
tnt: j tnt
halt
