; Determines the max value in an array and then halts

; Non-trivial halting programs are tricky in Sphinx.  Unlike max.s, we
; will not be able to make use of Sphinx's predictive powers, but we can
; still write a conventional algorithm to finds the max value.
; Also, although we can write programs that either halt or not halt for
; any arbitrarily complicated reason, if we want the program to produce
; arbitrary output based on a computation and then halt, it becomes
; necessary to use non-static jumps (along the real path of execution,
; all jumps must be taken in a halting program, but that doesn't mean
; that the same jump always always needs to go to the same place).

; So the strategy in writing non-trivial halting Sphinx programs is to
; turn your conditionals into a boolean 0 or 1 and then look up the
; address to jump to based on that.

; Currently I haven't added bitwise operators, but we don't need 'em
; To test if a number is non-zero (0 if 0, 1 if non-zero):
;   mov [test], 0
;   div [test], [x], [x]
;  OR with the value to test in test:
;   div [test], [test], [test]

; To test if a number is positive (1 if positive/zero, 0 negative)
;   add [test], [x], 1
;   div [test], [test], [x]


%format word 2
%section const
arr: .word 1, 3, 5, 4, 2
end_arr:

; Because we have less than 256 instructions, we can get away with bytes
; rather than words, which means we don't need to multiply by 1w just to
; look up something in this table, and can just use lbco directly.
branch_done:
    .byte not_done
    .byte done
branch_bigger:
    .byte continue
    .byte bigger

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
    sub [diff], [addr], end_arr
    add [jump], [diff], 1
    div [jump], [jump], [diff]
    lbco [jump], branch_done, [jump]
    j [jump]
    halt
    not_done:

    lwc [cur_val], [addr]

    ; TLE [cur_val], [max_val]
    ; B continue
    ; (Ok, this is actually a TGE, but who cares)
    sub [diff], [cur_val], [max_val]
    add [jump], [diff], 1
    div [jump], [jump], [diff]
    lbco [jump], branch_bigger, [jump]
    j [jump]
    halt
    bigger:

    mov [max_val], [cur_val]

    continue:
    add [addr], [addr], 1w
j loop
halt

done:
yield [max_val]
