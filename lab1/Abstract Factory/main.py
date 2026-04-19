from abc import ABC, abstractmethod

class Chair(ABC):
    @abstractmethod
    def sit_on(self) -> str:
        pass

class Sofa(ABC):
    @abstractmethod
    def lie_on(self) -> str:
        pass

class ModernChair(Chair):
    def sit_on(self) -> str:
        return "You sat down on a minimalist modern chair."

class ModernSofa(Sofa):
    def lie_on(self) -> str:
        return "You are lying on a sleek modern sofa."

class VictorianChair(Chair):
    def sit_on(self) -> str:
        return "You sat down on a fancy Victorian chair."

class VictorianSofa(Sofa):
    def lie_on(self) -> str:
        return "You are lying on a luxurious Victorian sofa."

class FurnitureFactory(ABC):
    @abstractmethod
    def create_chair(self) -> Chair:
        pass

    @abstractmethod
    def create_sofa(self) -> Sofa:
        pass

class ModernFurnitureFactory(FurnitureFactory):
    def create_chair(self) -> Chair:
        return ModernChair()
    
    def create_sofa(self) -> Sofa:
        return ModernSofa()

class VictorianFurnitureFactory(FurnitureFactory):
    def create_chair(self) -> Chair:
        return VictorianChair()
    
    def create_sofa(self) -> Sofa:
        return VictorianSofa()

def client_service(factory: FurnitureFactory):
    chair = factory.create_chair()
    sofa = factory.create_sofa()
    
    print(chair.sit_on())
    print(sofa.lie_on())

print("--- Client orders Modern furniture ---")
client_service(ModernFurnitureFactory())

print("\n--- Client orders Victorian furniture ---")
client_service(VictorianFurnitureFactory())