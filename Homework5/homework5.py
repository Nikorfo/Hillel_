class Character:
    max_hp = 100    
    def __init__(self, name: str, max_hp: int):
        self.name   = name
        self.max_hp = max_hp
        self.hp     = max_hp
    def hp(self) -> int:
        return self.hp

    
    def take_damage(self, amount: int) -> None:
        self.hp = max( 0, self.hp - amount )

    def heal(self, amount: int) -> None:
        self.hp = min( self.max_hp, self.hp + amount)

    def is_alive(self) -> bool:
        return self.hp > 0

Rimuru = Character("Hero", 120)    
Rimuru.take_damage(40)
print(Rimuru.hp)
Rimuru.heal(60)
print(Rimuru.hp)
Rimuru.take_damage(400)
print(Rimuru.hp)
print(Rimuru.is_alive)

Rimuru.hp = 999