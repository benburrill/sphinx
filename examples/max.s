; Finds the max value of an array, returning as soon as it's encountered

%format word 2
%section const
arr: .word 9, 8, 7, 6, 5
end_arr:

%section state
max_val: .word 0
cur_val: .word 0
addr: .word arr + 1w

%section code
mov [max_val], {arr}

j found_max
loop:
hge [addr], end_arr
    lwc [cur_val], [addr]

    j continue
    hle [cur_val], [max_val]

    mov [max_val], [cur_val]
    j found_max

    continue:
    add [addr], [addr], 1w
j loop
halt

found_max:
yield [max_val]
flag done
tnt: j tnt
halt
