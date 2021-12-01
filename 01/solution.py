with open('input.txt') as f:
    numbers = f.readlines()

increases = 0
first = int(numbers[0])
for i in numbers[1:]:
    second = int(i)
    if second > first:
        increases += 1
    first = second

print(increases)

increases = 0
numbers = [int(i) for i in numbers]
i = 0
first = sum(numbers[i:i+3])
for i in range(len(numbers) - 3):
    second = sum(numbers[i+1:i+4])
    if second > first:
        increases += 1
    first = second

print(increases)
