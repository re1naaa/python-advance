class Student:
    def __init__(self, name, age):
        #initialize privat attribute
        self.__name=name
        self.__age=age

    def get_name(self):
            return self.__name

    def set_name(self,name):
            self.__name=name

    def get_age(self):
            return self.__age

    def set_age(self, age):
            self.__age=age

student12= Student("Dion", 17)

print("Name", student12.get_name())
student12.set_name("Egzon")
print("Updated Name", student12.get_name())

print("Age", student12.get_age())
student12.set_age(18)
print("Updated Age:", student12.get_age())

