from project import message

greeting = "Hello"
name = "Reina"

def greet_2():
    global greeting
    greeting = "Goodbye"

    name = "Erion"

    message = f"{greeting}, {name}!"

    print(message)

greet_2()

print(greeting)

print(name)