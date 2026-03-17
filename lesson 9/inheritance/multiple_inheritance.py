class Vertebrate:
    def __init__(self, backbone=True):
        self.has_backbone = backbone

    def vertebrate_info(self):
        print("Vertebrates have a backbone")

class Aquantic:
    def __init__(self, habitat="water"):
        self.habitat=habitat

    def aquantic_info(self):
        print("Aquantic animals live in water")


class Fish(Vertebrate, Aquantic):
    def __init__(self, species, backbone=True, habitat="water"):
        super().__init__(backbone=backbone)
        self.habitat=habitat
        self.species=species

    def fish_info(self):
        print(f"The {self.species} is a type of fish found in {self.habitat}.")

    def swim(self):
        print("The fish is swimming")

goldfish = Fish("Goldfish")
print(goldfish.has_backbone)
print(goldfish.habitat)
goldfish.vertebrate_info()
goldfish.aquantic_info()
goldfish.fish_info()
goldfish.swim()