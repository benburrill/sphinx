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


; ----------------------------------------------------------------------
; Side note: Another similar case is one in which we update some state
; (eg increment a counter) in main.  With finite state, this doesn't
; change anything: the counter would eventually wrap around, so not
; jumping would not lead to halting for one of the future jumps (because
; in order to reach that state, we would have already decided not to
; jump at the same state, so we must not jump).
;
; However, if we attempt to generalize to infinite state (ie by setting
; %format word inf) we have a non-repeating loop.  By permitting such
; non-repeating execution, we essentially lose determinism, as it would
; seemingly become entirely consistent for j i_will_halt to do anything,
; so long as i_will_halt halts.  I'm not sure if there might be some way
; to regain determinism, but I suspect not in general, and in any case
; you'd probably need to change the meaning of what the jump instruction
; does to some extent.
;
; Of course %format word inf was already broken to begin with, since
; determining whether or not to jump with an infinite word size requires
; deciding the undecidable, but here we see a more direct way in which
; Sphinx fundamentally requires finitely bounded state in order to work.
