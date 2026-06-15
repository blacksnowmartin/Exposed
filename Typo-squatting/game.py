import random
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class Item(ABC):
    """Abstract base class enforcing Object-Oriented design patterns for items."""
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    @abstractmethod
    def get_description(self) -> str:
        pass

class Cyberware(Item):
    """Equippable modification items boosting operational stats."""
    def __init__(self, name: str, stat_bonus: int, slot: str, value: int):
        super().__init__(name, value)
        self.stat_bonus = stat_bonus
        self.slot = slot  # "Neural", "Ocular", "Somatic"

    def get_description(self) -> str:
        return f"[{self.slot}] {self.name} (+{self.stat_bonus} Engine Output)"

class Consumable(Item):
    """Single-use recovery or enhancement payloads."""
    def __init__(self, name: str, heal_amount: int, value: int):
        super().__init__(name, value)
        self.heal_amount = heal_amount

    def get_description(self) -> str:
        return f"[Consumable] {self.name} (Restores {self.heal_amount} Integrity)"

class Entity(ABC):
    """Abstract parent class managing core spatial and biological data structures."""
    def __init__(self, name: str, max_hp: int, attack_power: int):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_power = attack_power

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        actual_damage = max(1, amount)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

class Player(Entity):
    """Primary system loop controller representing the human operator."""
    def __init__(self, name: str):
        super().__init__(name, max_hp=100, attack_power=15)
        self.credits: int = 50
        self.xp: int = 0
        self.level: int = 1
        self.inventory: List[Item] = [Consumable("Standard Nano-Med", 40, 15)]
        self.equipment: Dict[str, Optional[Cyberware]] = {
            "Neural": None, "Ocular": None, "Somatic": None
        }

    def get_total_attack(self) -> int:
        bonus = sum(item.stat_bonus for item in self.equipment.values() if item)
        return self.attack_power + bonus

    def gain_xp(self, amount: int) -> bool:
        self.xp += amount
        xp_needed = self.level * 50
        if self.xp >= xp_needed:
            self.xp -= xp_needed
            self.level += 1
            self.max_hp += 20
            self.hp = self.max_hp
            self.attack_power += 5
            return True
        return False

    def equip(self, item: Cyberware) -> Optional[Cyberware]:
        old_item = self.equipment[item.slot]
        self.equipment[item.slot] = item
        return old_item

class RogueAI(Entity):
    """Algorithmic threat vectors scaling with node structural deepness."""
    def __init__(self, node_depth: int):
        names = ["Bit-Crusher", "Logic-Leech", "Net-Stalker", "Quantum-Wraith"]
        name = f"{random.choice(names)} v{node_depth}.0"
        
        # Exponential scaling logic mapping linearly to higher threat matrix profiles
        hp = random.randint(40, 60) + (node_depth * 12)
        atk = random.randint(8, 14) + (node_depth * 4)
        
        super().__init__(name, max_hp=hp, attack_power=atk)
        self.xp_reward = 20 + (node_depth * 10)
        self.credit_reward = random.randint(15, 35) + (node_depth * 5)

class GameEngine:
    """The central state-machine running core evaluation matrices."""
    def __init__(self):
        print("Initializing Cyber-Grid Terminal...")
        time.sleep(0.5)
        self.player = Player(input("Enter Operator Alias: ").strip() or "Anon_User")
        self.current_depth = 1

    def run(self):
        print(f"\nWelcome to the Grid, {self.player.name}. Breach protocol initialized.")
        while self.player.is_alive:
            self.show_dashboard()
            choice = input("\n[M]ove Deeper | [I]nventory | [Q]uit -> ").upper().strip()
            
            if choice == 'M':
                self.encounter_node()
            elif choice == 'I':
                self.manage_inventory()
            elif choice == 'Q':
                print("Disconnecting safely. State unmapped.")
                break
            else:
                print("Invalid command. Connection unstable.")
        
        if not self.player.is_alive:
            print("\n>>> CRITICAL SYSTEM FAILURE: BRAIN DUMP COMPLETE. GAME OVER. <<<")

    def show_dashboard(self):
        print("\n" + "=" * 50)
        print(f" OPERATOR: {self.player.name} | LVL: {self.player.level} ({self.player.xp}/{self.player.level*50} XP)")
        print(f" INTEGRITY: {self.player.hp}/{self.player.max_hp} | CREDITS: {self.player.credits}¢")
        print(f" CURRENT LAYER: Node Sub-Grid {self.current_depth}")
        print("-" * 50)
        for slot, item in self.player.equipment.items():
            eq_name = item.name if item else "Empty"
            print(f"  {slot} Slot: {eq_name}")
        print("=" * 50)

    def encounter_node(self):
        print(f"\nSlicing through Node {self.current_depth}...")
        time.sleep(0.7)
        event = random.random()

        if event < 0.60:
            self.combat_loop(RogueAI(self.current_depth))
        elif event < 0.85:
            self.loot_node()
        else:
            print("Safe sector detected. Local subroutines quiet.")
            self.player.credits += random.randint(5, 15)
            
        self.current_depth += 1

    def combat_loop(self, enemy: RogueAI):
        print(f"\n⚠️ ICE BREACH! Intrusion counter-measures active: {enemy.name} detected!")
        
        while enemy.is_alive and self.player.is_alive:
            print(f"\nYour Integrity: {self.player.hp}/{self.player.max_hp} | {enemy.name}: {enemy.hp}/{enemy.max_hp}")
            action = input("[A]ttack Program | [U]se Consumable -> ").upper().strip()

            if action == 'A':
                # Player attacks
                dmg = random.randint(self.player.get_total_attack() - 3, self.player.get_total_attack() + 3)
                inflicted = enemy.take_damage(dmg)
                print(f">> Executed attack: Inflicted {inflicted} corruption to {enemy.name}.")
                
                if enemy.is_alive:
                    # Enemy counter attacks
                    e_dmg = random.randint(enemy.attack_power - 2, enemy.attack_power + 2)
                    rec = self.player.take_damage(e_dmg)
                    print(f"<< Warning: {enemy.name} fires feedback loop! Sustained {rec} damage.")
            
            elif action == 'U':
                self.use_consumable_in_combat()
            else:
                print("Mis-input. CPU cycles wasted! Enemy exploits delay.")
                rec = self.player.take_damage(enemy.attack_power)
                print(f"Sustained {rec} damage.")

        if self.player.is_alive:
            print(f"\nTarget scrubbed. Gained {enemy.xp_reward} XP and {enemy.credit_reward}¢.")
            self.player.credits += enemy.credit_reward
            if self.player.gain_xp(enemy.xp_reward):
                print("🌟 SOFTWARE UPDATE COMPLETE: Operator efficiency parameters increased!")

    def loot_node(self):
        print("\n🎁 Encrypted Data Cache found! Decoupling locks...")
        time.sleep(0.5)
        
        if random.random() < 0.4:
            items = [
                Cyberware("Neural Link v2", 6, "Neural", 40),
                Cyberware("Threat Scanner", 8, "Ocular", 55),
                Cyberware("Myoelectric Fiber", 10, "Somatic", 70)
            ]
            dropped = random.choice(items)
        else:
            dropped = Consumable("Hyper-Med Kit", 75, 30)

        print(f"Recovered: {dropped.get_description()}")
        self.player.inventory.append(dropped)

    def manage_inventory(self):
        while True:
            print("\n--- Cargo Bay / Inventory Manifest ---")
            if not self.player.inventory:
                print("No items in localized arrays.")
                break
                
            for idx, item in enumerate(self.player.inventory):
                print(f" [{idx}] {item.get_description()}")
            
            choice = input("\nEnter index to use/equip, or [B]ack -> ").strip()
            if choice.upper() == 'B' or not choice:
                break
                
            if choice.isdigit() and int(choice) < len(self.player.inventory):
                item = self.player.inventory.pop(int(choice))
                if isinstance(item, Consumable):
                    self.player.hp = min(self.player.max_hp, self.player.hp + item.heal_amount)
                    print(f"Injected {item.name}. System stability optimized.")
                    break
                elif isinstance(item, Cyberware):
                    old = self.player.equip(item)
                    print(f"Mounted {item.name} into {item.slot} slot.")
                    if old:
                        self.player.inventory.append(old)
                        print(f"Returned {old.name} to general inventory inventory.")
                    break
            else:
                print("Array out of bounds or bad command.")

    def use_consumable_in_combat(self):
        consumables = [i for i in self.player.inventory if isinstance(i, Consumable)]
        if not consumables:
            print("No medical patches left in quick-slots!")
            return
            
        item = consumables[0]
        self.player.inventory.remove(item)
        self.player.hp = min(self.player.max_hp, self.player.hp + item.heal_amount)
        print(f"System patched via {item.name}. Integrity up by {item.heal_amount}.")

if __name__ == "__main__":
    try:
        engine = GameEngine()
        engine.run()
    except KeyboardInterrupt:
        print("Execution interrupted. Shutting down safely.")
