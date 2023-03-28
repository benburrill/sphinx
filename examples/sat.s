; An O(n) SAT solver

%format output byte
%section const
; (A|B|C) & (~A|~B|~C) & (~A|B) & (~B|A) & -A
formula:
.word A, B, C, 0
.word -A, -B, -C, 0
.word -A, B, 0
.word -B, A, 0
.word -A, 0
end_formula:

%section state
; Ensure vars != 0 by putting a word before it
addr: .word vars
vars:
A: .word 0, 'A'
B: .word 0, 'B'
C: .word 0, 'C'
end_vars:

temp: .word 0
sign: .word 0
result: .word 0

%section code
j unsat

yield '['
loop:
hge [addr], end_vars
    j keep
    lwso [temp], [addr], 1w
    yield [temp]
    sws [addr], 1
    keep:

    add [addr], [addr], 2w
j loop
yield ']'
yield '\n'

; Ok this is arguably bit of a lie, but if we reach this point, we have
; already found and outputted a satisfying solution, we just then need
; to go through the steps of actually evaluating it.
flag done

mov [result], 0
mov [addr], formula
evaluate:
    lwc [temp], [addr]
    j update
    hne [temp], 0
    and [result], [result], 1
    heq [result], 0
    mov [result], 0
    j continue
    halt

    update:
    heq [temp], 0
    asr [sign], [temp], 8w
    xor [temp], [temp], [sign]
    sub [temp], [temp], [sign]
    lws [temp], [temp]
    xor [temp], [temp], [sign]
    or [result], [result], [temp]

    continue:
    add [addr], [addr], 1w
j evaluate
hlt [addr], end_formula

tnt: j tnt
halt

unsat:
flag unsatisfiable
flag done
