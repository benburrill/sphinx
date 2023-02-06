; Example of self-inquiry, and the importance of determinism in Sphinx

; This program performs a kind of self-inquiry.
; j main / halt is an unconditional jump to the start of the program.
; The state is identical to when it started, so in essence, when we do 
; j i_will_halt, we are asking whether this program will halt, and may
; then act on that information in the case that it will halt.
;
; This seems a bit concerning, but it isn't.  The answer to whether this
; program will halt is no.  The i_will_halt branch will never be taken
; and we will never be able to produce a contradiction, nor could there
; be multiple valid paths of execution.
;
; What j i_will_halt is really asking is specifically if not jumping
; would lead to halting.  If it doesn't jump on j i_will_halt, then by
; virtue of determinism, it can never jump in the same state, which
; makes the self-inquiry into a trivial infinite loop -- which means
; that not jumping won't lead to halting.  So it won't jump.
main:
j i_will_halt
j main
halt



i_will_halt:
; It does not matter if this leads to a halt or not - the jump to here
; will never be taken
