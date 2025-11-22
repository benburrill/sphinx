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
lbc [value], [ip]
sbs [dp], [value]
add [ip], [ip], 1
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
j end_bracket_0_1
begin_bracket_0_1:
lbs [value], [dp]
heq [value], 0
lbs [value], [dp]
sub [value], [value], 1
sbs [dp], [value]
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
add [dp], [dp], 1
j begin_bracket_0_1
end_bracket_0_1:
lbs [value], [dp]
hne [value], 0
sub [dp], [dp], 1
j end_bracket_0_2
begin_bracket_0_2:
lbs [value], [dp]
heq [value], 0
lbs [value], [dp]
yield [value]
j begin_bracket_0_2
end_bracket_0_2:
lbs [value], [dp]
hne [value], 0
flag done
tnt: j tnt
halt
