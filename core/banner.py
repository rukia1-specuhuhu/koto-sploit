"""Banner and ASCII art for Kotosploit"""

import random
from colorama import Fore, Style
from core.ascii_cats import get_random_cat, get_hacker_cat

BANNER = r"""
 _  __     _                 _       _ _   
| |/ /    | |               | |     (_) |  
| ' / ___ | |_ ___  ___ _ __| | ___  _| |_ 
|  < / _ \| __/ _ \/ __| '_ \ |/ _ \| | __|
| . \ (_) | || (_) \__ \ |_) | | (_) | | |_ 
|_|\_\___/ \__\___/|___/ .__/|_|\___/|_|\__|
                       | |                  
                       |_|                  
"""

def get_random_fact():
    facts = [
        f"{Fore.CYAN}Weather: {random.choice(['Rainy', 'Sunny', 'Cloudy', 'Purr-fect', 'Meow-velous', 'Hackstorm'])}{Style.RESET_ALL}",
        f"{Fore.YELLOW}Caffeine Level: {random.randint(0, 100)}% (Cat nap needed: {random.randint(0, 100)}%){Style.RESET_ALL}",
        f"{Fore.GREEN}Weight: {random.uniform(3.5, 5.5):.1f}kg (Cat food consumed: {random.randint(1, 10)} bowls){Style.RESET_ALL}",
        f"{Fore.MAGENTA}Mood: {random.choice(['Playful', 'Sleepy', 'Hungry', 'Hacking', 'Purring', 'Stealthy', 'Curious'])}{Style.RESET_ALL}",
        f"{Fore.RED}Exploits Found: {random.randint(0, 42)} vulnerabilities (Mice caught: {random.randint(0, 20)}){Style.RESET_ALL}",
        f"{Fore.BLUE}Network Status: {random.choice(['Prowling', 'Scanning', 'Sniffing', 'Pouncing'])}{Style.RESET_ALL}",
        f"{Fore.CYAN}Energy: {random.randint(0, 100)}% (Yarn balls played with: {random.randint(0, 15)}){Style.RESET_ALL}",
    ]
    return random.sample(facts, 3)

def display_banner():
    print(f"{Fore.RED}{BANNER}{Style.RESET_ALL}")
    cat_art = get_random_cat() if random.random() > 0.3 else get_hacker_cat()
    print(f"{Fore.CYAN}{cat_art}{Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
    for fact in get_random_fact():
        print(f"  {fact}")
    print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}  Web Penetration Testing Framework{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  Type 'help' for available commands{Style.RESET_ALL}\n")
