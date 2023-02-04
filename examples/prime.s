%format word 2
%section const
; Good test cases: 437 = 19*23, 439 = 1*439
number: .word 439

%section state
test: .word 2
mod_result: .word 0

%section code
j composite
flag will_be_prime
test_divis:
    mod [mod_result], {number}, [test]
    heq [mod_result], 0
    add [test], [test], 1
    j test_divis
    hlt [test], {number}

flag prime
j done
halt

composite: flag composite
done: flag done
tnt: j tnt
halt
