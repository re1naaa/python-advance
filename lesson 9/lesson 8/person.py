class Person:
    def __init__(self, name, age):
        self.name=name
        self.age=age

    def greet(self):
        print(f"Hello, I am {self.name}, amd I am {self.age} years old.")

person1 = Person("Festa", 15)
person2 = Person("Egzon", 17)

person1.greet()
person2.greet()