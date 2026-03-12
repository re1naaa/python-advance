def calculate_area(lenght, width):
    return lenght * width

def calculate_perimeter(length, width):
    return 2 *(length+width)

length = 5
width = 3

area = calculate_area(length, width)
perimeter = calculate_perimeter(length, width)

print(f"Area: {area}")
print(f"Perimeter: {perimeter}")

