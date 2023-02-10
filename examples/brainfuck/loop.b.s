%section const
input: .asciiz ""
%section state
value: .word 0
ip: .word input
dp: .word data
data: .zero 1000
%section code
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
j end_bracket_0_1
begin_bracket_0_1:
lbs [value], [dp]
heq [value], 0
lbs [value], [dp]
yield [value]
j begin_bracket_0_1
end_bracket_0_1:
lbs [value], [dp]
hne [value], 0
flag done
tnt: j tnt
halt
