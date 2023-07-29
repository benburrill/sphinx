; Find all primes less than max_number.
; This code uses a simple primality test, which skips the effort of
; testing if the number is prime if it is composite.  If the number will
; turn out to be prime, the work of actually testing if it is prime is
; done _after_ the number is outputted.  However, since the work still
; needs to be done before moving on to the next number in the loop, we
; aren't really saving any time in the prime case.
;
; Although simple, and demonstrating some aspects of Sphinx programming,
; there are much better ways to do primality tests in Sphinx.
; See factor.s for a better algorithm.  The primality test there is only
; slightly more code than what's used here, but is O(log(N)) rather than
; O(N).  However, it's harder to reason about.  Another difference is in
; factor.s, primes are found immediately, whereas here it is composites
; which are found immediately.

%format word 2
%section const
max_number: .word 100

%section state
number: .word 2
test: .word 0
mod_result: .word 0

%section code
yield 2  ; Because my code skips it
loop:
    add [number], [number], 1

    ; We're guaranteed a path to an infinite loop here, so this is only
    ; testing if [number] >= {max_number}, nothing else.
    j done
    hgt [number], {max_number}

    j loop             ; if composite, try a new one
    yield [number]     ; we know it's gonna be prime, so output it
    mov [test], 2
    test_divis:
        mod [mod_result], [number], [test]
        heq [mod_result], 0
        add [test], [test], 1
    j test_divis
    hlt [test], [number]
j loop
halt

done: flag done
tnt: j tnt
halt
