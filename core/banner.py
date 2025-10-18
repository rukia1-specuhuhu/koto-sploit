import random
import datetime
from colorama import Fore, Style
from core.ascii_cats import get_random_cat, get_hacker_cat
from core.config import Config

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
        f"{Fore.YELLOW}Supporters: {random.randint(0, 100)}% (Special thanks to yuri08){Style.RESET_ALL}",
    ]
    return random.sample(facts, 3)

def get_supporters():
    supporters = [
        {
            "name": "yuri08",
            "role": "Developer",
            "contribution": "framework development and security research"
        },
    ]
    return supporters

def get_system_info():
    system_info = [
        f"{Fore.GREEN}OS: {random.choice(['Linux', 'Windows', 'macOS', 'FreeBSD'])} (Cat-approved){Style.RESET_ALL}",
        f"{Fore.BLUE}Python: {random.choice(['3.8', '3.9', '3.10', '3.11'])}.{random.randint(0, 9)} (Snake charmer){Style.RESET_ALL}",
        f"{Fore.YELLOW}Memory: {random.randint(4, 64)}GB (Plenty of space for cat naps){Style.RESET_ALL}",
        f"{Fore.RED}CPU: {random.choice(['Intel', 'AMD', 'ARM'])} {random.randint(2, 16)} cores (Purring at {random.randint(1000, 5000)}MHz){Style.RESET_ALL}",
        f"{Fore.CYAN}Storage: {random.choice(['SSD', 'HDD', 'NVMe')} {random.randint(256, 2048)}GB (Enough space for cat videos){Style.RESET_ALL}",
    ]
    return random.sample(system_info, 3)

def get_hacker_quote():
    quotes = [
        "\"The only truly secure system is one that is powered off, cast in a block of concrete and sealed in a lead-lined room with armed guards.\" - Gene Spafford",
        "\"Know your enemy and know yourself and you can fight a hundred battles without disaster.\" - Sun Tzu (adapted for hackers)",
        "\"Hackers are not just people who break into systems. They are people who enjoy the intellectual challenge of overcoming limitations.\" - Richard Stallman",
        "\"The cat could very well be man's best friend, but would never stoop to admitting it.\" - Doug Larson",
        "\"Curiosity killed the cat, but satisfaction brought it back.\" - yuri08",
        "\"In a world full of mice, be a cat.\" - yuri08",
        "\"Hack like a cat, silent but deadly.\" - kotosploit team",
    ]
    return random.choice(quotes)

def display_banner():
    print(f"{Config.BANNER_COLOR}{BANNER}{Style.RESET_ALL}")
    
    cat_choice = random.random()
    if cat_choice < 0.7:  
        cat_art = get_random_cat()
    elif cat_choice < 0.9:  
        cat_art = get_hacker_cat()
    else:  
        cat_art = """
    /\\_/\\  
   ( >^.^< ) 
    \\_____/ 
     |   |
    /|___|\\
        """
    
    print(f"{Config.CAT_ART_COLOR}{cat_art}{Style.RESET_ALL}")
    
    print(f"\n{Config.FACT_COLOR}{'='*60}{Style.RESET_ALL}")
    
    for fact in get_random_fact():
        print(f"  {fact}")
    
    print(f"{Config.FACT_COLOR}{'='*60}{Style.RESET_ALL}\n")
    
    print(f"{Config.FRAMEWORK_INFO_COLOR}Special thanks to our supporters:{Style.RESET_ALL}")
    supporters = get_supporters()
    for supporter in supporters:
        print(f"  {Config.SUPPORTER_NAME_COLOR}{supporter['name']}{Style.RESET_ALL} - {Config.SUPPORTER_ROLE_COLOR}{supporter['role']}{Style.RESET_ALL}")
        print(f"    {Config.SUPPORTER_CONTRIBUTION_COLOR}{supporter['contribution']}{Style.RESET_ALL}")
    
    print(f"\n{Config.FACT_COLOR}{'='*60}{Style.RESET_ALL}\n")
    
    print(f"{Config.FRAMEWORK_INFO_COLOR}System Information:{Style.RESET_ALL}")
    for info in get_system_info():
        print(f"  {info}")
    
    print(f"{Config.FACT_COLOR}{'='*60}{Style.RESET_ALL}\n")
    
    print(f"{Config.FRAMEWORK_INFO_COLOR}  {Config.FRAMEWORK_DESCRIPTION}{Style.RESET_ALL}")
    print(f"{Config.COMMAND_COLOR}  Type 'help' for available commands{Style.RESET_ALL}\n")
    
    print(f"{Fore.BLUE}  {Config.get_version_string()}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  'Purr-fect security assessment tool'{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}  {get_hacker_quote()}{Style.RESET_ALL}\n")
