; Find the sum of an array, but output 0 immediately if it will be 0
%format word 2
%section const
arr: .word 2, 3, -8, 3
end_arr:

%section state
sum: .word 0
addr: .word arr
temp: .word 0

%section code
j show_result
loop:
    j end_loop
    hge [addr], end_arr

    lwc [temp], [addr]
    add [addr], [addr], 1w
    add [sum], [sum], [temp]
j loop
halt

end_loop:
hlt [addr], end_arr
heq [sum], 0
show_result:
yield [sum]
flag done
tnt: j tnt
halt
