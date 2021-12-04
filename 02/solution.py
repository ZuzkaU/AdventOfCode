with open('input.txt') as f:
    rows = f.readlines()

distance=0
depth=0
for r in rows:
    Rule=r.split()[0]
    Number=int(r.split()[1])
    if Rule=='forward':
        distance += Number
    elif Rule=='down':
        depth += Number
    elif Rule=='up':
        depth -= Number

print(distance*depth)


aim=0
distance=0
depth=0
for r in rows:
    Rule=r.split()[0]
    Number=int(r.split()[1])
    if Rule=='forward':
        distance += Number
        depth += aim*Number
    elif Rule=='down':
        aim += Number
    elif Rule=='up':
        aim -= Number

print(distance*depth)
