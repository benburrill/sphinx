%format output byte
%section const
input: .asciiz "This is some input"
%section state
value: .word 0
ip: .word input
dp: .word data
data: .zero 1000
%section code
lbc [value], [ip]
sbs [dp], [value]
add [ip], [ip], 1
j end_bracket_0_1
begin_bracket_0_1:
lbs [value], [dp]
heq [value], 0
lbs [value], [dp]
yield [value]
lbc [value], [ip]
sbs [dp], [value]
add [ip], [ip], 1
j begin_bracket_0_1
end_bracket_0_1:
lbs [value], [dp]
hne [value], 0
flag done
tnt: j tnt
halt
