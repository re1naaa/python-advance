from email.policy import default


def person(name, greeting="Hello"):
    message= f"{greeting}, {name}"
    return message

default_greeting = person("Erion")
custom_greeting = person("Reina", "Hi")

print(default_greeting)
print(custom_greeting)