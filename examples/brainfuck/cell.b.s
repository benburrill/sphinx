%argv [<input>]
%format output byte
%section const
input: .arg input ascii
.byte 0
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
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_0_1
end_bracket_0_1:
lbs [value], [dp]
hne [value], 0
add [dp], [dp], 1
j end_bracket_0_2
begin_bracket_0_2:
lbs [value], [dp]
heq [value], 0
sub [dp], [dp], 1
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
add [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_0_2
end_bracket_0_2:
lbs [value], [dp]
hne [value], 0
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
sub [dp], [dp], 1
j end_bracket_0_3
begin_bracket_0_3:
lbs [value], [dp]
heq [value], 0
add [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
sub [dp], [dp], 1
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
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_1_1
end_bracket_1_1:
lbs [value], [dp]
hne [value], 0
add [dp], [dp], 1
j end_bracket_1_2
begin_bracket_1_2:
lbs [value], [dp]
heq [value], 0
sub [dp], [dp], 1
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
add [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_1_2
end_bracket_1_2:
lbs [value], [dp]
hne [value], 0
sub [dp], [dp], 1
j end_bracket_1_3
begin_bracket_1_3:
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
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_1_3
end_bracket_1_3:
lbs [value], [dp]
hne [value], 0
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
add [dp], [dp], 1
j end_bracket_1_4
begin_bracket_1_4:
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
j end_bracket_2_1
begin_bracket_2_1:
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
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_2_1
end_bracket_2_1:
lbs [value], [dp]
hne [value], 0
add [dp], [dp], 1
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
j end_bracket_2_2
begin_bracket_2_2:
lbs [value], [dp]
heq [value], 0
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_2_2
end_bracket_2_2:
lbs [value], [dp]
hne [value], 0
sub [dp], [dp], 1
sub [dp], [dp], 1
j end_bracket_2_3
begin_bracket_2_3:
lbs [value], [dp]
heq [value], 0
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_2_3
end_bracket_2_3:
lbs [value], [dp]
hne [value], 0
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
add [dp], [dp], 1
j begin_bracket_1_4
end_bracket_1_4:
lbs [value], [dp]
hne [value], 0
sub [dp], [dp], 1
j end_bracket_1_5
begin_bracket_1_5:
lbs [value], [dp]
heq [value], 0
add [dp], [dp], 1
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
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
j end_bracket_2_4
begin_bracket_2_4:
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
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_2_4
end_bracket_2_4:
lbs [value], [dp]
hne [value], 0
add [dp], [dp], 1
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
yield [value]
j end_bracket_2_5
begin_bracket_2_5:
lbs [value], [dp]
heq [value], 0
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_2_5
end_bracket_2_5:
lbs [value], [dp]
hne [value], 0
sub [dp], [dp], 1
sub [dp], [dp], 1
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_1_5
end_bracket_1_5:
lbs [value], [dp]
hne [value], 0
j begin_bracket_0_3
end_bracket_0_3:
lbs [value], [dp]
hne [value], 0
add [dp], [dp], 1
j end_bracket_0_4
begin_bracket_0_4:
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
j end_bracket_1_6
begin_bracket_1_6:
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
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_1_6
end_bracket_1_6:
lbs [value], [dp]
hne [value], 0
add [dp], [dp], 1
lbs [value], [dp]
yield [value]
j end_bracket_1_7
begin_bracket_1_7:
lbs [value], [dp]
heq [value], 0
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_1_7
end_bracket_1_7:
lbs [value], [dp]
hne [value], 0
sub [dp], [dp], 1
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_0_4
end_bracket_0_4:
lbs [value], [dp]
hne [value], 0
sub [dp], [dp], 1
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
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
j end_bracket_0_5
begin_bracket_0_5:
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
j begin_bracket_0_5
end_bracket_0_5:
lbs [value], [dp]
hne [value], 0
add [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
add [dp], [dp], 1
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
sub [dp], [dp], 1
lbs [value], [dp]
yield [value]
add [dp], [dp], 1
add [dp], [dp], 1
lbs [value], [dp]
yield [value]
lbs [value], [dp]
add [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
add [value], [value], 1
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
sub [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
add [dp], [dp], 1
add [dp], [dp], 1
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
lbs [value], [dp]
yield [value]
j end_bracket_0_6
begin_bracket_0_6:
lbs [value], [dp]
heq [value], 0
j end_bracket_1_8
begin_bracket_1_8:
lbs [value], [dp]
heq [value], 0
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
j begin_bracket_1_8
end_bracket_1_8:
lbs [value], [dp]
hne [value], 0
sub [dp], [dp], 1
j begin_bracket_0_6
end_bracket_0_6:
lbs [value], [dp]
hne [value], 0
flag done
tnt: j tnt
halt
