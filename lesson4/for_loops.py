names = ["medina", "andi", "reina", "egzon"]

for name in names:
    print(name)

    sentence = "Hello, world"

    for character in sentence:

        if character.isalpha():
            print(character)

    for numbers in range(1, 9):
        print(numbers)

numbers = [12, 33, 44, 55, 666, 77, 7, 8]

maximum = numbers[0]

for num in numbers:
    if num > maximum:
        maximum = num
        print("the biggest number in this list is :" ,maximum)