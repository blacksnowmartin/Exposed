import random
import time
import sys

class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def type_print(text, speed=0.007):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()


def prompt(message, valid_options=None):
    while True:
        choice = input(message).strip().lower()
        if valid_options is None or choice in valid_options:
            return choice
        print(f"{Color.YELLOW}Invalid option. Try again.{Color.END}")


class Item:
    def __init__(self, name, item_type, value, weight):
        self.name = name
        self.item_type = item_type
        self.value = value
        self.weight = weight

    def __repr__(self):
        return self.name


class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.floor = 1
        self.max_hp = 100
        self.hp = self.max_hp
        self.armor = 5
        self.weapon = Item("Thermal Blade", "weapon", 15, 2)
        self.credits = 150
        self.nanites = 3
        self.inventory = [Item("Hypo-Strap", "medical", 40, 1)]
        self.buffs = []

    def is_alive(self):
        return self.hp > 0

    def get_attack_damage(self):
        base = self.weapon.value + random.randint(-2, 4)
        if any(buff == "overclock" for buff in self.buffs):
            base = int(base * 1.25)
        return max(1, base)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount):
        self.hp -= amount
        self.hp = max(0, self.hp)

    def add_item(self, item):
        self.inventory.append(item)
        type_print(f"{Color.CYAN}{item.name} added to inventory.{Color.END}")

    def use_medical(self):
        medical = next((item for item in self.inventory if item.item_type == "medical"), None)
        if medical:
            self.heal(medical.value)
            self.inventory.remove(medical)
            type_print(f"{Color.GREEN}💊 Used {medical.name}. Restored {medical.value} HP.{Color.END}")
            return True
        type_print(f"{Color.RED}No medical supplies left.{Color.END}")
        return False

    def show_stats(self):
        inventory_names = ", ".join([item.name for item in self.inventory]) or "Empty"
        print(f"\n{Color.BOLD}--- {self.name.upper()} // SYSTEM STATUS ---{Color.END}")
        print(f"Level: {Color.CYAN}{self.level}{Color.END} | Floor: {Color.CYAN}{self.floor}/6{Color.END}")
        print(f"HP: {Color.GREEN}{self.hp}/{self.max_hp}{Color.END} | Armor: {Color.CYAN}{self.armor}{Color.END}")
        print(f"Credits: {Color.YELLOW}₵{self.credits}{Color.END} | Nanites: {Color.CYAN}{self.nanites}{Color.END}")
        print(f"Weapon: {Color.RED}{self.weapon.name} (DMG: {self.weapon.value}){Color.END}")
        print(f"Inventory: {inventory_names}")
        print("-" * 45)


class Enemy:
    TEMPLATES = [
        {"name": "Scrap Drone", "hp": 40, "power": 10, "reward": 30},
        {"name": "Corpo Enforcer", "hp": 55, "power": 13, "reward": 45},
        {"name": "Netrunner Phantom", "hp": 45, "power": 12, "reward": 40},
        {"name": "Cyber-Psycho", "hp": 65, "power": 18, "reward": 60},
    ]

    def __init__(self, floor):
        template = random.choice(self.TEMPLATES if floor < 6 else [{"name": "Megacorp AI Core", "hp": 120, "power": 24, "reward": 150}])
        self.name = template["name"]
        self.max_hp = template["hp"] + (floor * 5)
        self.hp = self.max_hp
        self.power = template["power"] + (floor * 2)
        self.reward = template["reward"] + (floor * 10)

    def attack(self, player):
        damage = max(1, self.power - player.armor + random.randint(-2, 3))
        player.take_damage(damage)
        return damage


class GameEngine:
    def __init__(self):
        print(f"{Color.MAGENTA}{Color.BOLD}INITIALIZING CYBER-PULSE NEURAL MATRIX...{Color.END}")
        time.sleep(1)
        self.player = None
        self.running = True

    def boot_sequence(self):
        print("\n" * 2)
        type_print(f"{Color.CYAN}====== NEO-BABYLON: UNDERGROUND 2088 ======{Color.END}", 0.03)
        type_print("A neon metropolis of corporate secrets and augmented assassins awaits below.")
        username = input(f"\nEnter your Hacker/Merc alias: {Color.BOLD}").strip()
        print(Color.END, end="")
        if not username:
            username = "V_Anon"
        self.player = Player(username)
        type_print(f"\nLink established. Welcome to the grid, {self.player.name}.")
        type_print("Infiltrate the Corporate Spire, survive the floors, and reclaim your freedom.")

    def generate_room(self):
        events = ["combat", "combat", "merchant", "secure_cache", "glitch_node"]
        return random.choice(events)

    def execute_combat(self):
        enemy = Enemy(self.player.floor)
        type_print(f"\n{Color.RED}⚠️ ALERT: {enemy.name} detected in sector {self.player.floor}!{Color.END}")

        while enemy.hp > 0 and self.player.is_alive():
            print(f"\n{Color.BOLD}{enemy.name}{Color.END} | HP: {enemy.hp}/{enemy.max_hp} | Power: {enemy.power}")
            print(f"Your HP: {Color.GREEN}{self.player.hp}/{self.player.max_hp}{Color.END}")
            choice = prompt(
                f"Actions: ({Color.BOLD}A{Color.END})ttack | ({Color.BOLD}M{Color.END})edical | ({Color.BOLD}F{Color.END})lee: ",
                {"a", "m", "f"}
            )

            if choice == 'a':
                damage = self.player.get_attack_damage()
                crit = random.random() < 0.18
                if crit:
                    damage = int(damage * 1.5)
                    type_print(f"{Color.YELLOW}CRITICAL STRIKE! {damage} damage dealt.{Color.END}")
                else:
                    type_print(f"You strike the {enemy.name} for {damage} damage.")
                enemy.hp -= damage
                enemy.hp = max(0, enemy.hp)

                if enemy.hp > 0:
                    counter = enemy.attack(self.player)
                    type_print(f"{Color.RED}{enemy.name} counters for {counter} damage.{Color.END}")

            elif choice == 'm':
                self.player.use_medical()

            elif choice == 'f':
                if random.random() < 0.45:
                    type_print(f"{Color.GREEN}Escape successful. You slip into the shadows.{Color.END}")
                    return
                counter = enemy.attack(self.player)
                type_print(f"Escape failed. {enemy.name} hits you for {counter} damage.{Color.END}")

        if self.player.is_alive():
            type_print(f"\n{Color.GREEN}Target down. Loot acquired: ₵{enemy.reward}.{Color.END}")
            self.player.credits += enemy.reward
            if random.random() < 0.45:
                loot = random.choice([
                    Item("Sub-Dermal Plating", "cyberware", 4, 1),
                    Item("Plasma Pistol", "weapon", 28, 4),
                    Item("Nano-Stimulator", "medical", 30, 1)
                ])
                self.handle_loot(loot)

    def handle_loot(self, item):
        type_print(f"{Color.CYAN}Scavenged: {item.name}.{Color.END}")
        if item.item_type == 'weapon':
            choice = prompt(f"Equip {item.name} instead of {self.player.weapon.name}? (y/n): ", {'y', 'n'})
            if choice == 'y':
                self.player.weapon = item
                type_print("Weapon hot-swapped.")
            else:
                self.player.add_item(item)
        elif item.item_type == 'cyberware':
            self.player.armor += item.value
            type_print(f"Armor increased by {item.value}. Current armor: {self.player.armor}.")
        elif item.item_type == 'medical':
            self.player.add_item(item)

    def enter_merchant(self):
        type_print(f"\n{Color.YELLOW}🏪 Black-market node online. Choose carefully.{Color.END}")
        while True:
            print(f"Credits: ₵{self.player.credits}")
            print("1. Nano-Shield Upgrade (+3 Armor) -> ₵60")
            print("2. Hypo-Strap Injection Pack (+40 HP item) -> ₵40")
            print("3. Monowire Lash (Weapon, 35 DMG) -> ₵120")
            print("4. Neural Cache Refill (Restore 20% HP) -> ₵80")
            print("5. Leave node.")
            choice = prompt("Choose purchase: ", {'1', '2', '3', '4', '5'})
            if choice == '1':
                if self.player.credits >= 60:
                    self.player.credits -= 60
                    self.player.armor += 3
                    type_print("Armor plating upgraded.")
                else:
                    type_print("Insufficient credits.")
            elif choice == '2':
                if self.player.credits >= 40:
                    self.player.credits -= 40
                    self.player.add_item(Item("Hypo-Strap", "medical", 40, 1))
                else:
                    type_print("Insufficient credits.")
            elif choice == '3':
                if self.player.credits >= 120:
                    self.player.credits -= 120
                    self.player.weapon = Item("Monowire Lash", "weapon", 35, 1)
                    type_print("Monowire synced to your neural rig.")
                else:
                    type_print("Insufficient credits.")
            elif choice == '4':
                if self.player.credits >= 80:
                    self.player.credits -= 80
                    restore = int(self.player.max_hp * 0.2)
                    self.player.heal(restore)
                    type_print(f"Restored {restore} HP.")
                else:
                    type_print("Insufficient credits.")
            else:
                type_print("Node disengaged.")
                break

    def secure_cache(self):
        if random.random() < 0.25:
            damage = random.randint(8, 18)
            self.player.take_damage(damage)
            type_print(f"{Color.RED}Trap triggered! {damage} damage sustained while hacking the cache.{Color.END}")
        else:
            reward = random.randint(40, 100)
            self.player.credits += reward
            type_print(f"{Color.GREEN}Cache breached. +₵{reward} collected.{Color.END}")
            if random.random() < 0.3:
                item = Item("Regen Injector", "medical", 50, 1)
                self.player.add_item(item)

    def glitch_node(self):
        if random.random() < 0.5:
            buff = "overclock"
            self.player.buffs.append(buff)
            type_print(f"{Color.MAGENTA}Your systems overclocked. Next attack is stronger.{Color.END}")
        else:
            damage = random.randint(5, 14)
            self.player.take_damage(damage)
            type_print(f"{Color.RED}System glitch backfired: {damage} damage taken.{Color.END}")

    def level_up(self):
        self.player.level += 1
        self.player.max_hp += 10
        self.player.hp = min(self.player.max_hp, self.player.hp + 15)
        self.player.armor += 1
        type_print(f"{Color.CYAN}Advancing through the Spire has hardened your systems. Level {self.player.level}.{Color.END}")

    def revive_if_needed(self):
        if not self.player.is_alive() and self.player.nanites > 0:
            choice = prompt(f"{Color.YELLOW}Nanite package detected. Consume one to restore 60 HP? (y/n): {Color.END}", {'y', 'n'})
            if choice == 'y':
                self.player.nanites -= 1
                self.player.hp = 60
                type_print(f"{Color.GREEN}Nanite repair engaged. HP restored to 60.{Color.END}")
                return True
        return False

    def run_game(self):
        self.boot_sequence()
        while self.running and self.player.is_alive():
            self.player.show_stats()
            print(f"\n{Color.BOLD}[SECTOR {self.player.floor} OF 6]{Color.END}")
            action = prompt(f"Commands: ({Color.BOLD}M{Color.END})ove forward | ({Color.BOLD}Q{Color.END})uit: ", {'m', 'q'})
            if action == 'q':
                type_print("Disconnecting neural uplink. Stay hidden.")
                break
            room = self.generate_room()
            if room == 'combat':
                self.execute_combat()
            elif room == 'merchant':
                self.enter_merchant()
            elif room == 'secure_cache':
                self.secure_cache()
            elif room == 'glitch_node':
                self.glitch_node()

            if self.player.is_alive():
                self.player.floor += 1
                self.level_up()
                if self.player.floor > 6:
                    type_print(f"\n{Color.YELLOW}🎉 Surface access achieved. The Corporate Spire has fallen. Freedom is yours.{Color.END}")
                    self.running = False
            else:
                revived = self.revive_if_needed()
                if not revived:
                    type_print(f"{Color.RED}System failure. Your neural link collapses.{Color.END}")
                    break

        if self.player.is_alive() and not self.running:
            type_print(f"{Color.GREEN}Mission complete. {self.player.name} survived the Spire.{Color.END}")
        elif not self.player.is_alive():
            type_print(f"{Color.RED}Game over. The Spire consumed your signal.{Color.END}")


if __name__ == '__main__':
    GameEngine().run_game()
