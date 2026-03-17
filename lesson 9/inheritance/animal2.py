class Animal:
    def __init__(self, name):
        self.name=name

    def sound(self):
        print("Some generic animal sound")

    def descriptioin(self):
        print(f"This is a animal name {self.name}")

class Dog(Animal):
    def __init__(self,name,breed):
        super().__init__(name)
        self.breed = breed

    def sound(self):
        print("Woof!woof!")

    def descriptioin(self):
        super().descriptioin()

        print(f"Breed: {self.breed}")


class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    def sound(self):
        print("Meow!Meow!")

    def descriptioin(self):
        super().descriptioin()

        print(f"Color: {self.color}")

animal = Animal("Generic Animal")

animal.sound()
animal.descriptioin()

dog = Dog("Bella", "Golden Retriver")
dog.sound()
dog.descriptioin()

cat = Cat("Nimo", "White")
cat.sound()
cat.descriptioin()