import random
import time
import sys

class Color:
    """Terminal color sequences for an immersive UI experience."""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def type_print(text, speed=0.01):
    """Smooth, typewriter-style text presentation."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

class Item:
    def __init__(self, name, item_type, value, weight):
        self.name = name
        self.item_type = item_type  # 'weapon', 'cyberware', 'medical'
        self.value = value          # Damage for weapon, heal amount for medical, armor for cyberware
        self.weight = weight

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.credits = 150
        self.nanites = 3            # Revive / Emergency repair materials
        self.weapon = Item("Thermal Blade", "weapon", 15, 2)
        self.armor = 5              # Base structural defense
        self.inventory = [Item("Hypo-Strap", "medical", 40, 1)]
        self.floor = 1

    def is_alive(self):
        return self.hp > 0

    def show_stats(self):
        print(f"\n{Color.BOLD}--- {self.name.upper()} // SYSTEM STATUS ---{Color.END}")
        print(f"HP: {Color.GREEN}{self.hp}/{self.max_hp}{Color.END} | Armor: {Color.CYAN}{self.armor}{Color.END}")
        print(f"Credits: {Color.YELLOW}₵{self.credits}{Color.END} | Nanites: {Color.CYAN}{self.nanites}{Color.END}")
        print(f"Active Weapon: {Color.RED}{self.weapon.name} (DMG: {self.weapon.value}){Color.END}")
        print(f"Inventory: {[item.name for item in self.inventory]}")
        print("-" * 35)

class Enemy:
    def __init__(self, floor):
        names = ["Scrap Drone", "Corpo Enforcer", "Netrunner Phantom", "Cyber-Psycho"]
        self.name = random.choice(names) if floor < 5 else "Megacorp AI Core"
        self.hp = random.randint(30, 60) + (floor * 8)
        self.max_hp = self.hp
        self.damage = random.randint(8, 15) + (floor * 3)
        self.credits_reward = random.randint(20, 50) + (floor * 10)

class GameEngine:
    def __init__(self):
        print(f"{Color.CYAN}{Color.BOLD}INITIALIZING CYBER-PULSE NEURAL MATRIX...{Color.END}")
        time.sleep(1)
        self.player = None
        self.running = True

    def boot_sequence(self):
        print("\n" * 2)
        type_print(f"{Color.CYAN}====== NEO-BABYLON: UNDERGROUND 2088 ======{Color.END}", 0.03)
        username = input(f"\nEnter Hacker/Merc alias to link terminal: {Color.BOLD}").strip()
        print(Color.END, end="")
        if not username:
            username = "V_Anon"
        self.player = Player(username)
        type_print(f"\nConnection established. Welcome to the grid, {self.player.name}.\nEscape the Corporate Spire or perish.", 0.02)

    def generate_room(self):
        events = ["combat", "combat", "merchant", "secure_cache", "glitch_node"]
        return random.choice(events)

    def execute_combat(self):
        enemy = Enemy(self.player.floor)
        type_print(f"\n{Color.RED}⚠️ WARNING: Threat detected! {enemy.name} blocking progression!{Color.END}")
        
        while enemy.hp > 0 and self.player.is_alive():
            print(f"\nEnemy: {enemy.name} [HP: {enemy.hp}/{enemy.max_hp} | Power: {enemy.damage}]")
            print(f"Your HP: {self.player.hp}/{self.player.max_hp}")
            choice = input(f"Actions: ({Color.BOLD}A{Color.END})ttack | ({Color.BOLD}U{Color.END})se Hypo-Strap | ({Color.BOLD}F{Color.END})lee: ").lower().strip()
            
            if choice == 'a':
                # Player attacks
                crit = random.random() < 0.20
                dmg = self.player.weapon.value + random.randint(-3, 3)
                if crit:
                    dmg = int(dmg * 1.5)
                    type_print(f"{Color.YELLOW}💥 CRITICAL HIT! Overclocked protocols dealt {dmg} damage!{Color.END}")
                else:
                    type_print(f"You strike with your {self.player.weapon.name} for {dmg} damage.")
                enemy.hp -= dmg

                # Enemy counter-attacks if alive
                if enemy.hp > 0:
                    enemy_dmg = max(1, enemy.damage - self.player.armor + random.randint(-2, 2))
                    type_print(f"The {enemy.name} retaliates, bypassing systems to deal {enemy_dmg} damage.")
                    self.player.hp -= enemy_dmg

            elif choice == 'u':
                # Consume healing items via functional generator expression
                heal_item = next((item for item in self.player.inventory if item.item_type == "medical"), None)
                if heal_item:
                    self.player.hp = min(self.player.max_hp, self.player.hp + heal_item.value)
                    self.player.inventory.remove(heal_item)
                    type_print(f"{Color.GREEN}💊 Injected {heal_item.name}. Regenerated {heal_item.value} HP!{Color.END}")
                else:
                    type_print(f"{Color.RED}No healing items remaining in local memory!{Color.END}")
            
            elif choice == 'f':
                if random.random() < 0.40:
                    type_print(f"{Color.GREEN}Smoke-screen deployed. Successfully escaped battle!{Color.END}")
                    return
                else:
                    type_print(f"{Color.RED}Escape failed! Enemy intercepted your routing path!{Color.END}")
                    enemy_dmg = max(1, enemy.damage - self.player.armor)
                    self.player.hp -= enemy_dmg
            else:
                print("Invalid command packet.")

        if self.player.is_alive():
            type_print(f"\n{Color.GREEN}⚡ Target neutralized. Extracted ₵{enemy.credits_reward} from neural remnants.{Color.END}")
            self.player.credits += enemy.credits_reward
            if random.random() < 0.35:
                loot = Item("Sub-Dermal Plating", "cyberware", 4, 1) if random.random() < 0.5 else Item("Plasma Pistol", "weapon", 28, 4)
                type_print(f"{Color.CYAN}Scavenged functional hardware: {loot.name}!{Color.END}")
                self.player.inventory.append(loot)
                self.manage_loot(loot)

    def manage_loot(self, item):
        if item.item_type == "weapon":
            swap = input(f"Equip {item.name} over your current {self.player.weapon.name}? (y/n): ").lower().strip()
            if swap == 'y':
                self.player.weapon = item
                type_print("Weapon arrays hot-swapped.")
        elif item.item_type == "cyberware":
            self.player.armor += item.value
            type_print(f"Cyberware fused. Passive armor permanently raised by +{item.value}.")

    def enter_merchant(self):
        type_print(f"\n{Color.YELLOW}🏪 Found Net-Runner black-market node.{Color.END}")
        print(f"Your Credits: ₵{self.player.credits}")
        print(f"1. Nano-Shield Upgrade (+3 Armor) -> ₵60")
        print(f"2. Hypo-Strap Injection Pack (+40 HP item) -> ₵40")
        print(f"3. Monowire Lash (Weapon - 35 DMG) -> ₵120")
        print(f"4. Leave node link.")
        
        choice = input("Select structural purchase: ").strip()
        if choice == '1' and self.player.credits >= 60:
            self.player.armor += 3
            self.player.credits -= 60
            print("System armor hardened.")
        elif choice == '2' and self.player.credits >= 40:
            self.player.inventory.append(Item("Hypo-Strap", "medical", 40, 1))
            self.player.credits -= 40
            print("Hypo-Strap loaded to inventory array.")
        elif choice == '3' and self.player.credits >= 120:
            self.player.weapon = Item("Monowire Lash", "weapon", 35, 1)
            self.player.credits -= 120
            print("Monowire synced to neural interface.")
        else:
            type_print("Transaction terminated or insufficient funds.")

    def run_game(self):
        self.boot_sequence()
        
        while self.running and self.player.is_alive():
            self.player.show_stats()
            print(f"\n{Color.BOLD}[SOCIETY TERMINAL LEVEL: {self.player.floor}/5]{Color.END}")
            action = input(f"Commands: ({Color.BOLD}M{Color.END})ove Forward | ({Color.BOLD}Q{Color.END})uit Matrix: ").lower().strip()
            
            if action == 'q':
                type_print("Disconnecting neural uplink safely. Goodbye.")
                break
            elif action == 'm':
                room_type = self.generate_room()
                if room_type == "combat":
                    self.execute_combat()
                elif room_type == "merchant":
                    self.enter_merchant()
                elif room_type == "secure_cache":
                    found_credits = random.randint(30, 80)
                    self.player.credits += found_credits
                    type_print(f"\n{Color.GREEN}🔓 Hacked a secure cargo safe! Decrypted ₵{found_credits}!{Color.END}")
                elif room_type == "glitch_node":
                    damage = random.randint(5, 15)
                    self.player.hp -= damage
                    type_print(f"\n{Color.RED}⚡ Environmental Hazard! Suffered a severe data feedback loop loop for {damage} damage!{Color.END}")

                # Check level progression logic
                if self.player.is_alive():
                    self.player.floor += 1
                    if self.player.floor > 5:
                        type_print(f"\n{Color.YELLOW}🎉 SYSTEM PURIFIED! You reached the surface mainframe and secured your freedom!{Color.END}")
                        self.running = False
            else:
                print("Unknown dynamic syntax option.")

            # Hard death/revive algorithm loop via nanite fallback
            if not self.player.is_alive() and self.player.nanites > 0:
