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
; In designing a high level language that compiles to Sphinx, we want to
; be able to have features that will allow us, hopefully rather neatly,
; to write a true interpreter for sphinxfuck.
;
; NOTE: sphinxfuck programs which terminate are not run properly by this
; interpreter, and I do not think they should be a focus in trying to
; come up with high-level language features.  It should be possible to
; run through the execution of terminating sphinxfuck programs (so long
; as the interpreter ends in terminal non-termination), but it would
; take a bit more work, as I think we'd need a separate execution mode
; that the interpreter would enter if it detects that the program that
; it is running would halt.
; The problem is basically that halt propagation causes halting programs
; to halt before they even start, so while they have the correct halting
; behavior, they do not produce any output.

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
; prog: .ascii "++++++++[(!>++++[(!>++>+++>+++>+<<<<-])?>+>+>->>+[(!<])?<-])?>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.@(]"
end_prog:
input: .asciiz ""
%section state
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
        heq [value], 0
    j inc
    halt

    hnz:
    hne [instr], '?'
        lbs [value], [dp]
        hne [value], 0
    j inc
    halt

    jback:
    hne [instr], ']'
        j head_back
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

end_of_prog:
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
