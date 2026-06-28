# CYBERNEON: VOID PROTOCOL
# A cyberpunk hacking simulation game for terminal warriors
# Neon aesthetics, procedural elements, skill-based hacking mini-games

import os
import sys
import time
import random
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich import box
import threading

console = Console()

# Neon color palette
NEON_GREEN = "#39FF14"
NEON_CYAN = "#00F9FF"
NEON_MAGENTA = "#FF00FF"
NEON_PURPLE = "#9D00FF"
NEON_ORANGE = "#FF6600"
NEON_RED = "#FF0033"
NEON_YELLOW = "#FFFF00"

class Player:
    def __init__(self):
        self.username = "ghost_7"
        self.level = 1
        self.exp = 0
        self.exp_to_level = 100
        self.skills = {
            "brute_force": 1,
            "crypto": 1,
            "stealth": 1,
            "exploit": 1,
            "social_eng": 1
        }
        self.bandwidth = 100
        self.cpu = 100
        self.detection_risk = 0
        self.inventory = ["basic_shell", "dictionary_attack", "proxy_chain", "signal_scrambler", "bandwidth_booster"]
        self.achievements = []
        self.current_node = "entry_point"
        self.proxy_active = False

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.exp_to_level = int(self.exp_to_level * 1.5)
        for skill in self.skills:
            self.skills[skill] += 1
        console.print(f"\n[bold {NEON_GREEN}]LEVEL UP! You are now level {self.level}[/]")

    def reduce_detection(self, amount):
        self.detection_risk = max(0, self.detection_risk - amount)

    def restore_bandwidth(self, amount):
        self.bandwidth = min(100, self.bandwidth + amount)

    def restore_cpu(self, amount):
        self.cpu = min(100, self.cpu + amount)

class Node:
    def __init__(self, name, difficulty, security_level, data_value, node_type="generic"):
        self.name = name
        self.difficulty = difficulty
        self.security_level = security_level
        self.data_value = data_value
        self.node_type = node_type
        self.hacked = False
        self.connections = []
        self.alerted = False

class Game:
    def __init__(self):
        self.player = Player()
        self.nodes = self.generate_network()
        self.game_over = False
        self.score = 0
        self.story_progress = 0

    def generate_network(self):
        nodes = {
            "entry_point": Node("ENTRY_POINT", 1, 2, 50, node_type="gateway"),
            "mail_server": Node("MAIL_SERVER", 2, 3, 120, node_type="service"),
            "honeypot": Node("HONEYPOT", 3, 4, 80, node_type="trap"),
            "db_cluster": Node("DB_CLUSTER", 4, 5, 300, node_type="database"),
            "sandbox": Node("SANDBOX", 5, 6, 220, node_type="research"),
            "admin_panel": Node("ADMIN_PANEL", 6, 7, 500, node_type="control"),
            "ai_gateway": Node("AI_GATEWAY", 7, 8, 650, node_type="adaptive"),
            "core_router": Node("CORE_ROUTER", 8, 9, 800, node_type="infrastructure"),
            "vault": Node("VAULT", 10, 10, 2000, node_type="secure")
        }
        # Define connections
        nodes["entry_point"].connections = ["mail_server"]
        nodes["mail_server"].connections = ["db_cluster", "honeypot", "entry_point"]
        nodes["honeypot"].connections = ["mail_server"]
        nodes["db_cluster"].connections = ["admin_panel", "sandbox", "mail_server"]
        nodes["sandbox"].connections = ["db_cluster"]
        nodes["admin_panel"].connections = ["core_router", "db_cluster", "ai_gateway"]
        nodes["ai_gateway"].connections = ["admin_panel"]
        nodes["core_router"].connections = ["vault", "admin_panel"]
        nodes["vault"].connections = ["core_router"]
        return nodes

    def print_header(self):
        header = Text()
        header.append("█▄▀ █▀█ █▀▀ █░█ █▀█ █▀█ █▀", style=f"bold {NEON_CYAN}")
        header.append("  █░█ █▄█ █▄█ █▄█ █▀▄ █▄█ ▄█\n", style=f"bold {NEON_MAGENTA}")
        header.append(f"VOID PROTOCOL v0.8.4 | {self.player.username} | Level {self.player.level} | Score: {self.score}", style=NEON_GREEN)
        console.print(Panel(header, border_style=NEON_PURPLE, padding=(0, 2)))

    def show_status(self):
        table = Table(title="SYSTEM STATUS", box=box.SIMPLE, style=NEON_CYAN)
        table.add_column("Metric", style=NEON_GREEN)
        table.add_column("Value", justify="right")
        
        table.add_row("Bandwidth", f"[{'green' if self.player.bandwidth > 50 else 'red'}]{self.player.bandwidth}%[/]")
        table.add_row("CPU Load", f"[{'green' if self.player.cpu > 50 else 'red'}]{self.player.cpu}%[/]")
        table.add_row("Detection Risk", f"[{'green' if self.player.detection_risk < 40 else 'yellow' if self.player.detection_risk < 70 else 'red'}]{self.player.detection_risk}%[/]")
        table.add_row("Current Node", self.player.current_node.upper())
        table.add_row("Proxy Active", "[green]YES[/]" if self.player.proxy_active else "[red]NO[/]")
        table.add_row("Skills", ", ".join(f"{k}:{v}" for k, v in self.player.skills.items()))
        
        console.print(table)

    def scan_network(self):
        console.print(f"\n[{NEON_CYAN}]SCANNING NETWORK...[/]")
        with Progress() as progress:
            task = progress.add_task("[green]Probing nodes...", total=100)
            for _ in range(100):
                progress.update(task, advance=1)
                time.sleep(0.02)
        
        table = Table(title="CONNECTED NODES", box=box.DOUBLE)
        table.add_column("Node", style=NEON_GREEN)
        table.add_column("Difficulty", justify="center")
        table.add_column("Security", justify="center")
        table.add_column("Data Value", justify="right")
        table.add_column("Status", justify="center")
        
        for name, node in self.nodes.items():
            status = "[green]SECURE[/]" if not node.hacked else "[magenta]BREACHED[/]"
            table.add_row(
                name.upper(),
                str(node.difficulty),
                str(node.security_level),
                f"{node.data_value} creds",
                status
            )
        console.print(table)

    def connect_to_node(self, node_name):
        if node_name not in self.nodes:
            console.print(f"[{NEON_RED}]Node not found in network.[/]")
            return False

        allowed_routes = self.nodes[self.player.current_node].connections.copy()
        if self.player.proxy_active:
            allowed_routes += [node for node in self.nodes if node != self.player.current_node]

        if node_name not in allowed_routes:
            console.print(f"[{NEON_RED}]No direct route. Use proxy or scan first.[/]")
            return False
        
        if self.player.proxy_active:
            console.print(f"\n[{NEON_MAGENTA}]Proxy active: rerouting through safe channels...[/]")
            self.player.proxy_active = False
            self.player.reduce_detection(10)

        self.player.current_node = node_name
        console.print(f"\n[{NEON_CYAN}]Connected to {node_name.upper()}[/]")
        return True

    def use_tool(self, tool_name):
        if tool_name not in self.player.inventory:
            console.print(f"[{NEON_RED}]You do not have {tool_name} in your inventory.[/]")
            return False

        console.print(f"\n[{NEON_CYAN}]Activating {tool_name}...[/]")
        if tool_name == "basic_shell":
            self.player.skills["stealth"] += 1
            self.player.reduce_detection(10)
            self.player.restore_cpu(10)
            console.print(f"[{NEON_GREEN}]Basic shell stabilized. Stealth improved and detection reduced.[/]")
        elif tool_name == "signal_scrambler":
            self.player.reduce_detection(20)
            console.print(f"[{NEON_GREEN}]Signal noise increased. Detection risk lowered.[/]")
        elif tool_name == "bandwidth_booster":
            self.player.restore_bandwidth(30)
            self.player.restore_cpu(20)
            console.print(f"[{NEON_GREEN}]Bandwidth and CPU restored.[/]")
        elif tool_name == "proxy_chain":
            self.player.proxy_active = True
            console.print(f"[{NEON_GREEN}]Proxy chain established. Remote routing enabled.[/]")
        elif tool_name == "dictionary_attack":
            console.print(f"[{NEON_ORANGE}]Running dictionary reconnaissance...[/]")
            self.player.gain_exp(10)
            self.player.detection_risk += 5
            console.print(f"[{NEON_GREEN}]Weak credentials discovered. Brute force enhanced.[/]")
        else:
            console.print(f"[{NEON_YELLOW}]{tool_name} has no immediate effect.[/]")
        return True

    def print_help(self):
        console.print(Panel(
            "scan | connect <node> | hack | use <tool> | status | inventory | help | exit",
            title="COMMANDS", style=NEON_CYAN
        ))

    def brute_force_mini_game(self, node):
        console.print(f"\n[{NEON_ORANGE}]BRUTE FORCE INITIATED on {node.name}[/]")
        target_length = 6 + node.difficulty
        password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789!@#", k=target_length))
        
        console.print(f"[{NEON_GREEN}]Target hash length: {target_length}[/]")
        
        attempts = 0
        max_attempts = 12 - self.player.skills["brute_force"]
        if "dictionary_attack" in self.player.inventory:
            max_attempts += 1
        
        while attempts < max_attempts:
            guess = Prompt.ask(f"[{NEON_CYAN}]Enter password guess ({max_attempts - attempts} left)")
            attempts += 1
            
            if guess == password:
                console.print(f"[{NEON_GREEN}]ACCESS GRANTED! Password cracked.[/]")
                self.player.gain_exp(20 * node.difficulty)
                node.hacked = True
                self.score += node.data_value
                return True
            else:
                console.print(f"[{NEON_RED}]ACCESS DENIED[/] - {max_attempts - attempts} attempts left")
                self.player.detection_risk += 5
                self.player.cpu = max(0, self.player.cpu - 3)
        
        console.print(f"[{NEON_RED}]BRUTE FORCE FAILED. TRACE INITIATED.[/]")
        self.player.detection_risk += 25
        return False

    def crypto_puzzle(self, node):
        console.print(f"\n[{NEON_MAGENTA}]CRYPTO MODULE ENGAGED[/]")
        shift = random.randint(3, 13)
        plaintext = random.choice(["breach", "void", "neon", "ghost", "cipher", "shadow"])
        ciphertext = ''.join(chr((ord(c) - 97 + shift) % 26 + 97) if c.isalpha() else c for c in plaintext)
        
        console.print(f"[{NEON_CYAN}]Ciphertext: [bold]{ciphertext.upper()}[/] (Caesar shift unknown)[/]")
        
        guess = Prompt.ask("Decrypt the message")
        if guess.lower() == plaintext:
            console.print(f"[{NEON_GREEN}]CRYPTO BROKEN![/]")
            self.player.skills["crypto"] += 1
            self.player.gain_exp(25 * node.difficulty)
            node.hacked = True
            self.score += node.data_value * 2
            return True
        else:
            console.print(f"[{NEON_RED}]Decryption failed.[/]")
            self.player.detection_risk += 15
            self.player.cpu = max(0, self.player.cpu - 5)
            return False

    def exploit_node(self, node):
        console.print(f"\n[{NEON_ORANGE}]RUNNING EXPLOIT CHAIN on {node.name}[/]")
        
        base_chance = (self.player.skills["exploit"] * 8) + (100 - node.security_level * 4)
        if node.node_type == "secure":
            base_chance -= 10
        elif node.node_type == "trap":
            base_chance -= 15
        success_chance = min(95, max(15, base_chance))
        
        with Progress() as progress:
            task = progress.add_task("[red]Injecting payload...", total=100)
            for i in range(100):
                progress.update(task, advance=1)
                if random.random() < 0.05:
                    console.print(f"[{NEON_RED}]Anomaly detected![/]")
                time.sleep(0.03)
        
        if random.randint(1, 100) <= success_chance:
            console.print(f"[{NEON_GREEN}]EXPLOIT SUCCESSFUL! Root access acquired.[/]")
            node.hacked = True
            node.alerted = False
            self.player.gain_exp(30 * node.difficulty)
            self.score += int(node.data_value * 1.5)
            return True
        else:
            console.print(f"[{NEON_RED}]EXPLOIT PATCHED. IDS ALERT.[/]")
            self.player.detection_risk += 30
            self.player.cpu = max(0, self.player.cpu - 10)
            node.alerted = True
            return False

    def play(self):
        console.clear()
        self.print_header()
        console.print(Panel("[bold italic]Welcome to the grid, runner. The megacorps are watching.[/]", style=NEON_PURPLE))
        
        while not self.game_over:
            if self.player.detection_risk >= 100:
                console.print(f"\n[{NEON_RED}]DETECTION THRESHOLD BREACHED. NETSEC DRONES INCOMING.[/]")
                console.print("GAME OVER - You have been neutralized.")
                self.game_over = True
                break
            
            self.show_status()
            self.print_help()
            
            cmd = Prompt.ask("root@void", default="scan").strip().lower()
            parts = cmd.split()
            
            if cmd == "scan":
                self.scan_network()
            elif parts[0] == "connect" and len(parts) > 1:
                self.connect_to_node(parts[1])
            elif cmd == "hack":
                current = self.nodes[self.player.current_node]
                if current.hacked:
                    console.print(f"[{NEON_GREEN}]{self.player.current_node.upper()} already breached.[/]")
                    continue
                
                console.print(f"\n[{NEON_ORANGE}]SELECT ATTACK VECTOR:[/]")
                console.print("1. Brute Force")
                console.print("2. Cryptanalysis")
                console.print("3. Zero-Day Exploit")
                choice = Prompt.ask("Vector", choices=["1", "2", "3"])
                
                if choice == "1":
                    self.brute_force_mini_game(current)
                elif choice == "2":
                    self.crypto_puzzle(current)
                elif choice == "3":
                    self.exploit_node(current)
                
                if random.random() < 0.3:
                    self.player.detection_risk += random.randint(3, 12)
            elif parts[0] == "use" and len(parts) > 1:
                self.use_tool(parts[1])
            elif cmd == "status":
                self.show_status()
            elif cmd == "inventory":
                console.print(Panel(f"Tools: {', '.join(self.player.inventory)}", title="INVENTORY", style=NEON_CYAN))
            elif cmd == "help":
                self.print_help()
            elif cmd == "exit":
                if Confirm.ask("Disconnect from the grid?"):
                    break
            else:
                console.print(f"[{NEON_RED}]Unknown command. Type 'help' for more.[/]")
            
            hacked_count = sum(1 for n in self.nodes.values() if n.hacked)
            if hacked_count >= 4 and self.story_progress == 0:
                console.print(Panel("[bold magenta]The Vault is now within reach... Final target acquired.[/]", style=NEON_PURPLE))
                self.story_progress = 1
            
            if hacked_count >= 6 and self.story_progress == 1:
                console.print(Panel("[bold magenta]The system has weakened. The Vault is exposed. Finish strong.[/]", style=NEON_PURPLE))
                self.story_progress = 2
            
            time.sleep(0.3)

        console.print(f"\n[bold {NEON_GREEN}]FINAL TRANSMISSION[/]\nScore: {self.score} | Level: {self.player.level}")
        console.print("Thanks for playing CYBERNEON: VOID PROTOCOL")

if __name__ == "__main__":
    try:
        game = Game()
        game.play()
    except KeyboardInterrupt:
        console.print(f"\n[{NEON_RED}]Connection terminated by user.[/]")
    except Exception as e:
        console.print(f"[{NEON_RED}]CRITICAL ERROR: {e}[/]")