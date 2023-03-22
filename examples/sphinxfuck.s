; A "true" interpreter for sphinxfuck (hopefully)
; The idea with sphinxfuck is a brainfuck-style language using the same
; conditional-halt control flow as Sphinx.
;
; What I mean by a "true" interpreter is that the magic is implemented
; using magic rather than being emulated in any way (like the emulator
; for Sphinx).
;
; Instructions are like brainfuck, but [ jumps forward to matching ) if
; not jumping would lead to halting, ] jumps backwards to matching ( if
; not jumping would lead to halting, ! halts if value at data pointer is
; zero, ? halts if value at data pointer is non-zero, and @ produces the
; done flag.
;
; My hope is that it is possible in principle to convert Sphinx into
; sphinxfuck, though I'm not totally convinced by that since the way the
; ( and ) work in sphinxfuck is more restrictive than labels.  However,
; brainfuck gets away with something similar, so it's probably fine.
; Actually, I maybe could have skipped the whole parentheses thing since
; it doesn't give me true labels and a more brainfucky [ and ] probably
; would have worked just as well... but I'm not sure.  I think I'll just
; stick with the parentheses.
;
; It would be fairly easy to create a translator from sphinxfuck to
; Sphinx, similar to what I did for brainfuck, but an interpreter is
; more interesting because it is it is indirectly using halt-based jumps
; to implement halt-based jumps.
;
; Halting sphinxfuck programs will jump to reached_halt once they halt.
; This is accomplished through an alternative execution mode if halting
; is unavoidable.
;
; Programming in sphinxfuck:
; ?! is an unconditional halt (the end of the program is also)
;   Is that fitting punctuation for programming in sphinxfuck or what?!
; To translate brainfuck to sphinxfuck:
;   [ becomes [(! (or [!( if you don't care about halt propagation)
;   ] becomes ])? (or ]?) if you don't care about halt propagation)
;   Add @(] to the end for terminal non-termination
;   Everything else is the same

%format word 2
%section const
; Count to 255
; prog: .ascii "(.+]?@(]"

; Determine if a number is odd or even (1 if odd, 0 if even), outputting
; the answer immediately (before the number is even in memory), and then
; entering into an infinite loop.
; The input number is given by the number of pluses after the first @
; In the even case, the number of cycles still depends on the number of
; pluses because the interpreter needs to search forwards to find the
; matching ) - the number of cycles is the number of Sphinx instructions
; executed, not the number of sphinxfuck instructions.
prog: .ascii "[>+.<@+++++++++++++(!--]?!)>.<@(]"

; A hello world program translated from brainfuck
; %format output byte
; prog: .ascii "++++++++[(!>++++[(!>++>+++>+++>+<<<<-])?>+>+>->>+[(!<])?<-])?>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.@(]"

; An example halting sphinxfuck program
; prog: .ascii "(.+!]"
end_prog:
input: .asciiz ""
%section state
; In halt mode 0, halts are true halts.  If the program is guaranteed to
; halt, we switch to halt mode 1, where halts are virtualized.  In halt
; mode 1, halting instead jumps to reached_halt.
halt_mode: .word 0
pc: .word prog
ip: .word input
dp: .word data

; TODO: We should be able to reuse value and depth as the same word, but
; I can't be bothered right now.
instr: .word 0
value: .word 0
depth: .word 0

data: .zero 1000

%section code
mov [halt_mode], 1
; If we would halt under halt_mode 0, switch to halt_mode 1
j loop
mov [halt_mode], 0
loop:
j end_of_prog
hge [pc], end_prog
    lbc [instr], [pc]

    j left
    heq [instr], '<'
    j right
    heq [instr], '>'
    j add
    heq [instr], '+'
    j sub
    heq [instr], '-'
    j out
    heq [instr], '.'
    j in
    heq [instr], ','
    j hz
    heq [instr], '!'
    j hnz
    heq [instr], '?'
    j jback
    heq [instr], ']'
    j jfwd
    heq [instr], '['
    j flag
    heq [instr], '@'
    j inc
    halt


    left: 
    hne [instr], '<'
        sub [dp], [dp], 1
    j inc
    halt

    right:
    hne [instr], '>'
        add [dp], [dp], 1
    j inc
    halt

    add:
    hne [instr], '+'
        lbs [value], [dp]
        add [value], [value], 1
        sbs [dp], [value]
    j inc
    halt

    sub:
    hne [instr], '-'
        lbs [value], [dp]
        sub [value], [value], 1
        sbs [dp], [value]
    j inc
    halt

    out:
    hne [instr], '.'
        lbs [value], [dp]
        yield [value]
    j inc
    halt

    in:
    hne [instr], ','
        lbc [value], [ip]
        sbs [dp], [value]
        add [ip], [ip], 1
    j inc
    halt

    hz:
    hne [instr], '!'
        lbs [value], [dp]
        j hz_should_halt
        heq [value], 0
    j inc
    halt

    hz_should_halt:
    ; Jump to reached_halt if halt is virtualized, otherwise halt
    hne [value], 0
    heq [halt_mode], 0
    j reached_halt
    halt

    hnz:
    hne [instr], '?'
        lbs [value], [dp]
        j hnz_should_halt
        hne [value], 0
    j inc
    halt

    hnz_should_halt:
    ; Jump to reached_halt if halt is virtualized, otherwise halt
    heq [value], 0
    heq [halt_mode], 0
    j reached_halt
    halt

    jback:
    hne [instr], ']'
        j head_back
        ; If halts are virtualized, jump unconditionally
        hne [halt_mode], 0
        j inc
        halt

        head_back:
        mov [depth], 1

        find_back_stop:
            hle [depth], 0
            sub [pc], [pc], 1

            j no_back_stop
            hlt [pc], prog

            lbc [instr], [pc]

            j not_back_stop
            hne [instr], '('
                sub [depth], [depth], 1
            j continue_search_back
            halt

            not_back_stop:
            heq [instr], '('

            j not_back_jump
            hne [instr], ']'
                add [depth], [depth], 1
            j continue_search_back
            halt

            not_back_jump:
            heq [instr], ']'

        continue_search_back:
        j find_back_stop
        hgt [depth], 0
    j inc
    halt

    jfwd:
    hne [instr], '['
        j head_fwd
        ; If halts are virtualized, jump unconditionally
        hne [halt_mode], 0
        j inc
        halt

        head_fwd:
        mov [depth], 1

        find_fwd_stop:
            hle [depth], 0
            add [pc], [pc], 1

            j no_fwd_stop
            hge [pc], end_prog

            lbc [instr], [pc]

            j not_fwd_stop
            hne [instr], ')'
                sub [depth], [depth], 1
            j continue_search_fwd
            halt

            not_fwd_stop:
            heq [instr], ')'

            j not_fwd_jump
            hne [instr], '['
                add [depth], [depth], 1
            j continue_search_fwd
            halt

            not_fwd_jump:
            heq [instr], '['

        continue_search_fwd:
        j find_fwd_stop
        hgt [depth], 0
    j inc
    halt

    flag:
    hne [instr], '@'
        flag done
    j inc
    halt

    inc:
    add [pc], [pc], 1
j loop
halt

; Reaching the end of the program is an unconditional halt
end_of_prog:
heq [halt_mode], 0
j reached_halt
halt

no_back_stop:
hge [pc], prog
j error
halt
no_fwd_stop:
hlt [pc], end_prog
error:
flag error
tnt: j tnt
halt

reached_halt:
flag sphinxfuck_halt
; Because we make use of halt propagation for conditional branches in
; the implementation of sphinxfuck, although we may do anything we want
; after the sphinxfuck program halts, we must eventually reach tnt.
j tnt
halt
