; Find all primes less than max_number, skipping the effort of checking
; whether numbers are prime if they will just be composite (see prime.s)

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
