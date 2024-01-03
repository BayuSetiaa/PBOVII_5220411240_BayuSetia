class Peternakan:
    def __init__(self, name, health, attackPower, armorNumber):
        self.name = name
        self._health = health  
        self._attackPower = attackPower  
        self.__armorNumber = armorNumber  

    def showInfo(self):
        print('{} dengan Health = {}'.format(self.name, self._health))

    def serang(self, lawan):
        print(f"{self.name} menyerang!")
        lawan.diserang(self, self._attackPower)

    def diserang(self, lawan, attackPower_lawan):
        damage = attackPower_lawan - self.__armorNumber
        self._health -= damage
        print(f"{self.name} menerima serangan sebesar {damage} damage!")
        if self._health <= 0:
            print(f"{self.name} kalah!")

    def get_armor_number(self):
        return self.__armorNumber

    def set_armor_number(self, new_armor_number):
        if new_armor_number >= 0:
            self.__armorNumber = new_armor_number
        else:
            print("Nomor armor harus bernilai non-negatif.")


class Sapi(Peternakan):
    def __init__(self, name):
        super().__init__(name, 50, 10, 5)
        super().showInfo()

    def serang(self, lawan):
        print(f"{self.name} menyerang dengan Tanduk!")
        super().serang(lawan)

    def diserang(self, lawan, attackPower_lawan):
        print(f"{self.name} menerima serangan dari srigala!")
        super().diserang(lawan, attackPower_lawan)

    def teriakan_sapi(self):
        print(f"{self.name} berteriak moowww!")


class Srigala(Peternakan):
    def __init__(self, name):
        super().__init__(name, 100, 20, 10)
        super().showInfo()

    def serang(self, lawan):
        print(f"{self.name} menerkam sapi!")
        super().serang(lawan)

    def diserang(self, lawan, attackPower_lawan):
        print(f"{self.name} menerima serangan!")
        super().diserang(lawan, attackPower_lawan)

    def taring(self):
        print(f"{self.name} menggunakan taring untuk menyerang!")


class Peternak(Srigala):
    def __init__(self, name):
        super().__init__(name)
        self.special_attack_power = 30

    def cangkul_skill(self, lawan):
        print(f"{self.name} menyerang dengan cangkul!")
        lawan.diserang(self, self.special_attack_power)

    def senapan_skill(self):
        print(f"{self.name} menembak srigala dengan senapan!")



def battle_round(hero1, hero2):
    hero1.serang(hero2)
    hero2.serang(hero1)


sapi = Sapi('sapi')
srigala = Srigala('srigala')
peternak = Peternak('peternak')

ronde = 3

for round_num in range(1, ronde + 1):
    print(f"\nRound {round_num} of the Battle:")
    
    print("\nSapi attacks:")
    sapi.teriakan_sapi()
    battle_round(sapi, srigala)

    print("\nSrigala attacks:")
    srigala.taring()
    battle_round(srigala, sapi)
    battle_round(srigala, peternak)

    print("\nPeternak attacks:")
    peternak.senapan_skill()
    battle_round(peternak, srigala)

    round_winner = None
    if sapi._health > 0:
        round_winner = sapi.name
    elif srigala._health > 0:
        round_winner = srigala.name
    elif peternak._health > 0:
        round_winner = peternak.name

    if round_winner:
        print(f"\nRound {round_num} winner: {round_winner}")
    else:
        print(f"\nRound {round_num} is a draw!")

overall_winner = None
if sapi._health > 0:
    overall_winner = sapi.name
elif srigala._health > 0:
    overall_winner = srigala.name
elif peternak._health > 0:
    overall_winner = peternak.name

if overall_winner:
    print(f"\nOverall winner: {overall_winner}")
else:
    print("\nThe battle ended in a draw!")

print("\nTotal Health at the End:")
print(f"Sapi: {sapi._health}")
print(f"Srigala: {srigala._health}")
print(f"Peternak: {peternak._health}")