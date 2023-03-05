%format output byte
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
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
j end_bracket_0_1
begin_bracket_0_1:
lbs [value], [dp]
heq [value], 0
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
j end_bracket_1_1
begin_bracket_1_1:
lbs [value], [dp]
heq [value], 0
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
sub [dp], [dp], 1
sub [dp], [dp], 1
sub [dp], [dp], 1
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_1_1
end_bracket_1_1:
lbs [value], [dp]
hne [value], 0
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
add [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
add [dp], [dp], 1
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
j end_bracket_1_2
begin_bracket_1_2:
lbs [value], [dp]
heq [value], 0
sub [dp], [dp], 1
j begin_bracket_1_2
end_bracket_1_2:
lbs [value], [dp]
hne [value], 0
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_0_1
end_bracket_0_1:
lbs [value], [dp]
hne [value], 0
add [dp], [dp], 1
add [dp], [dp], 1
lbs [value], [dp]
yield [value]
add [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
lbs [value], [dp]
yield [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
add [dp], [dp], 1
add [dp], [dp], 1
lbs [value], [dp]
yield [value]
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
sub [dp], [dp], 1
lbs [value], [dp]
yield [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
add [dp], [dp], 1
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
flag done
tnt: j tnt
halt
