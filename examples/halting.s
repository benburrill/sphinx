; Determines the max value in an array and then halts

; Non-trivial halting programs are tricky in Sphinx.  Unlike max.s, we
; will not be able to make use of Sphinx's predictive powers, but we can
; still write a conventional algorithm to finds the max value.
; Also, although it's fairly easy to write programs that either halt or
; not halt for an arbitrarily complicated reason, if we want the program
; to produce arbitrary output based on a computation and then halt, we
; need to use non-static jumps (along the real path of execution, all
; jumps must be taken in a halting program, but that doesn't mean that
; the same jump always always needs to go to the same place).

; So the strategy in writing non-trivial halting Sphinx programs is to
; turn your conditionals into a boolean 0 or 1 and then look up the
; address to jump to based on that.

; Currently I haven't added bitwise operators, but we don't need 'em
; To test if x is non-zero (1 if non-zero, 0 if zero):
;   mov [test], [x]
;   div [test], [test], [test]

; Get sign of x (1 if positive, 0 if negative, 2 if zero):
;   add [test], [x], 1
;   add [temp], [x], 2
;   div [test], [temp], [test]

; To test if x is greater than or equal to y (assuming both positive):
;   div [test], [x], [y]
;   div [test], [test], [test]


%format word 2
%section const
; Because we have less than 256 instructions, we can get away with bytes
; rather than words, which means we don't need to multiply by 1w just to
; look up something in this table, and can just use lbco directly.
branch_done:
    .byte not_done
    .byte done
branch_sign:
    .byte continue ; diff < 0
    .byte bigger   ; diff > 0
    .byte continue ; diff = 0

arr: .word 1, 3, 5, 4, 2
end_arr:


%section state
jump: .word 0
diff: .word 0
max_val: .word 0
cur_val: .word 0
addr: .word arr + 1w

%section code
mov [max_val], {arr}

loop:
    ; TGE [addr], [end_arr]
    ; B done
    div [jump], [addr], end_arr
    ; No need to worry about addr > end_arr, so no need for another div
    lbco [jump], branch_done, [jump]
    j [jump]
    halt
    not_done:

    lwc [cur_val], [addr]

    ; TLE [cur_val], [max_val]
    ; B continue
    sub [diff], [cur_val], [max_val]
    add [jump], [diff], 1
    add [diff], [diff], 2
    div [jump], [diff], [jump]
    lbco [jump], branch_sign, [jump]
    j [jump]
    ; This halt is actually not necessary to ensure that the jump isn't
    ; skipped because the program is guaranteed to eventually halt due
    ; to the loop being bounded by the other jump (even if the program
    ; were to make the wrong decision here), so the correct jump will be
    ; taken here, with or without forcing it with an unconditional halt
    ; immediately after.  Easier to reason about with it though.
    ; Also means the emulator needs to do less work.
    halt
    bigger:

    mov [max_val], [cur_val]

    continue:
    add [addr], [addr], 1w
j loop
halt

done:
yield [max_val]
; Thanks to the power of unconditional conditional jumps, we don't need
; terminal non-termination to get the output to show!
