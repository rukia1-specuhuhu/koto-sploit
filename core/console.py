import os
import sys
from colorama import Fore, Style, init
from core.banner import display_banner
from core.module_loader import ModuleLoader
from modules.base import BaseModule

init(autoreset=True)

class KotosploitConsole:
    def __init__(self):
        self.loader = ModuleLoader()
        self.current_module = None
        self.prompt = f"{Fore.RED}kotosploit{Style.RESET_ALL} > "
        self.running = True
        
    def run(self):
        display_banner()
        while self.running:
            try:
                if self.current_module:
                    module_name = self.current_module.get_info()["name"]
                    prompt = f"{Fore.RED}kotosploit{Style.RESET_ALL}({Fore.CYAN}{module_name}{Style.RESET_ALL}) > "
                else:
                    prompt = self.prompt
                
                cmd = input(prompt).strip()
                if cmd:
                    self.process_command(cmd)
            except KeyboardInterrupt:
                print("\n")
                continue
            except EOFError:
                self.running = False
                print("\nExiting...")
    
    def process_command(self, cmd: str):
        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        commands = {
            "help": self.cmd_help,
            "show": self.cmd_show,
            "use": self.cmd_use,
            "back": self.cmd_back,
            "info": self.cmd_info,
            "set": self.cmd_set,
            "options": self.cmd_options,
            "run": self.cmd_run,
            "exploit": self.cmd_run,
            "search": self.cmd_search,
            "reload": self.cmd_reload,
            "exit": self.cmd_exit,
            "quit": self.cmd_exit,
            "banner": self.cmd_banner,
            "clear": self.cmd_clear,
        }
        
        if command in commands:
            commands[command](args)
        else:
            print(f"{Fore.RED}[!] Unknown command: {command}{Style.RESET_ALL}")
    
    def cmd_help(self, args):
        help_text = f"""
{Fore.YELLOW}Core Commands{Style.RESET_ALL}
{Fore.WHITE}{'='*60}{Style.RESET_ALL}
  help              Display this help menu
  show modules      List all available modules
  use <module>      Select a module to use
  back              Deselect current module
  info              Show module information
  set <opt> <val>   Set module option
  options           Show module options
  run/exploit       Execute the current module
  search <keyword>   Search modules by keyword
  reload            Reload all modules
  banner            Display banner again
  clear             Clear screen
  exit/quit         Exit Kotosploit

{Fore.YELLOW}Exploit Modules{Style.RESET_ALL}
{Fore.WHITE}{'='*60}{Style.RESET_ALL}
  exploit/sqli               SQL Injection scanner
  exploit/xss                Cross-Site Scripting detector
  exploit/lfi                Local File Inclusion scanner
  exploit/cmdi               Command Injection scanner
  exploit/openredirect        Open Redirect detector
  exploit/reflected-xss      Reflected XSS scanner
  exploit/stored-xss         Stored XSS scanner
  exploit/csrf               Cross-Site Request Forgery scanner
  exploit/xxe                 XML External Entity scanner
  exploit/xmli               XML Injection scanner
  exploit/nosqli              NoSQL Injection scanner
  exploit/ssrf                Server-Side Request Forgery scanner
  exploit/rfi                Remote File Inclusion scanner
  exploit/ssti                Server-Side Template Injection scanner
  exploit/code_injection      Code Injection scanner
  exploit/os-cmd-inj          OS Command Injection scanner
  exploit/ldapi               LDAP Injection scanner
  exploit/xpathinj            XPath Injection scanner
  exploit/cors                Cross-Origin Resource Sharing scanner
  exploit/crlfinjection       CRLF Injection scanner
  exploit/cache_poisoning     Cache Poisoning scanner
  exploit/follina             Follina vulnerability scanner
  exploit/foll                File/Object Local/Remote scanner
  exploit/weak_password_policy Weak Password Policy scanner
  exploit/passwordresetpoisoning Password Reset Poisoning scanner
  exploit/session_fixation    Session Fixation scanner
  exploit/session-hijacking   Session Hijacking scanner
  exploit/credentialstuffing  Credential Stuffing scanner
  exploit/clickjacking        Clickjacking scanner
  exploit/broken_authentication Broken Authentication scanner
  exploit/brokenauthz          Broken Authorization scanner
  exploit/business_logic       Business Logic Vulnerability scanner
  exploit/privilege_escalation Privilege Escalation scanner
  exploit/mobileapi            Mobile API Vulnerability scanner
  exploit/idor                 Insecure Direct Object Reference scanner
  exploit/forcedbrowsing      Forced Browsing scanner
  exploit/multiple             Multiple Vulnerability scanner

{Fore.YELLOW}Auxiliary Modules{Style.RESET_ALL}
{Fore.WHITE}{'='*60}{Style.RESET_ALL}
  auxiliary/dirfuzz         Directory/file fuzzing
  auxiliary/subdomain       Subdomain enumeration
  auxiliary/whois           WHOIS lookup
  auxiliary/headers         HTTP header analyzer
  auxiliary/ssl_scanner     SSL/TLS vulnerability scanner
  auxiliary/port_scanner    TCP port scanner
  auxiliary/db_scanner      Database service detector
  auxiliary/cms_detector    CMS detection & fingerprinting
  auxiliary/tech_stack      Technology stack detector
  auxiliary/info_disclosure Information disclosure scanner
  auxiliary/crawler         Web crawler for endpoints
  auxiliary/waf_detector     WAF detection & fingerprinting
  auxiliary/dns_scanner     DNS scanner
  auxiliary/email_scanner   Email harvester & validator
  auxiliary/subnet_scanner  Subnet scanner
  auxiliary/service_enum    Service enumeration

{Fore.YELLOW}Usage Example{Style.RESET_ALL}
{Fore.WHITE}{'='*60}{Style.RESET_ALL}
  kotosploit > use exploit/sqli
  kotosploit(SQLInjectionScanner) > set URL http://example.com/page
  kotosploit(SQLInjectionScanner) > set PARAM id
  kotosploit(SQLInjectionScanner) > run
"""
        print(help_text)
    
    def cmd_show(self, args):
        if args == "modules":
            modules = self.loader.list_modules()
            print(f"\n{Fore.YELLOW}Available Modules{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
            for path in sorted(modules.keys()):
                print(f"  {Fore.GREEN}{path}{Style.RESET_ALL}")
            print()
        else:
            print(f"{Fore.RED}[!] Usage: show modules{Style.RESET_ALL}")
    
    def cmd_use(self, args):
        if not args:
            print(f"{Fore.RED}[!] Usage: use <module_path>{Style.RESET_ALL}")
            return
        
        module = self.loader.get_module(args)
        if module:
            self.current_module = module
            print(f"{Fore.GREEN}[+] Loaded module: {args}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Module not found: {args}{Style.RESET_ALL}")
    
    def cmd_back(self, args):
        if self.current_module:
            self.current_module = None
            print(f"{Fore.GREEN}[+] Deselected module{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[*] No module selected{Style.RESET_ALL}")
    
    def cmd_info(self, args):
        if not self.current_module:
            print(f"{Fore.RED}[!] No module selected{Style.RESET_ALL}")
            return
        
        info = self.current_module.get_info()
        print(f"\n{Fore.YELLOW}Module Information{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"  Name:        {Fore.CYAN}{info['name']}{Style.RESET_ALL}")
        print(f"  Type:        {Fore.CYAN}{info['type']}{Style.RESET_ALL}")
        print(f"  Description: {Fore.CYAN}{info['description']}{Style.RESET_ALL}")
        print(f"  Author:      {Fore.CYAN}{info['author']}{Style.RESET_ALL}")
        print()
    
    def cmd_set(self, args):
        if not self.current_module:
            print(f"{Fore.RED}[!] No module selected{Style.RESET_ALL}")
            return
        
        parts = args.split(maxsplit=1)
        if len(parts) != 2:
            print(f"{Fore.RED}[!] Usage: set <option> <value>{Style.RESET_ALL}")
            return
        
        option, value = parts
        if self.current_module.set_option(option, value):
            print(f"{Fore.GREEN}[+] {option.upper()} => {value}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Invalid option: {option}{Style.RESET_ALL}")
    
    def cmd_options(self, args):
        if not self.current_module:
            print(f"{Fore.RED}[!] No module selected{Style.RESET_ALL}")
            return
        
        options = self.current_module.show_options()
        print(f"\n{Fore.YELLOW}Module Options{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}{'Name':<15} {'Value':<25} {'Required'}{Style.RESET_ALL}")
        print(f"  {'-'*15} {'-'*25} {'-'*8}")
        for name, value, required in options:
            print(f"  {name:<15} {value:<25} {required}")
        print()
    
    def cmd_run(self, args):
        if not self.current_module:
            print(f"{Fore.RED}[!] No module selected{Style.RESET_ALL}")
            return
        
        valid, msg = self.current_module.validate_options()
        if not valid:
            print(f"{Fore.RED}[!] {msg}{Style.RESET_ALL}")
            return
        
        print(f"{Fore.YELLOW}[*] Running module...{Style.RESET_ALL}\n")
        try:
            result = self.current_module.run()
            if result:
                self._display_results(result)
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
    
    def cmd_search(self, args):
        if not args:
            print(f"{Fore.RED}[!] Usage: search <keyword>{Style.RESET_ALL}")
            return
        
        keyword = args.lower()
        modules = self.loader.list_modules()
        matching_modules = []
        
        for path, module in modules.items():
            if keyword in path.lower():
                matching_modules.append(path)
        
        if matching_modules:
            print(f"\n{Fore.YELLOW}Matching Modules{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
            for path in sorted(matching_modules):
                print(f"  {Fore.GREEN}{path}{Style.RESET_ALL}")
            print()
        else:
            print(f"{Fore.YELLOW}[*] No modules found matching: {keyword}{Style.RESET_ALL}")
    
    def cmd_reload(self, args):
        print(f"{Fore.YELLOW}[*] Reloading modules...{Style.RESET_ALL}")
        self.loader = ModuleLoader()
        print(f"{Fore.GREEN}[+] Modules reloaded successfully{Style.RESET_ALL}")
    
    def _display_results(self, result):
        if result.get("success"):
            print(f"\n{Fore.GREEN}[+] Module execution completed{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[!] Module execution failed{Style.RESET_ALL}")
        
        if result.get("message"):
            print(f"{Fore.CYAN}{result['message']}{Style.RESET_ALL}")
        
        if result.get("vulnerabilities"):
            print(f"\n{Fore.YELLOW}Vulnerabilities Found:{Style.RESET_ALL}")
            for vuln in result.get("vulnerabilities"):
                print(f"  {Fore.RED}- {vuln.get('type', 'Unknown')}{Style.RESET_ALL}")
                if vuln.get("description"):
                    print(f"    {Fore.WHITE}{vuln.get('description')}{Style.RESET_ALL}")
        
        if result.get("exploits"):
            print(f"\n{Fore.YELLOW}Exploits Found:{Style.RESET_ALL}")
            for exploit in result.get("exploits"):
                print(f"  {Fore.RED}- {exploit.get('type', 'Unknown')}{Style.RESET_ALL}")
                if exploit.get("description"):
                    print(f"    {Fore.WHITE}{exploit.get('description')}{Style.RESET_ALL}")
    
    def cmd_exit(self, args):
        print(f"\n{Fore.YELLOW}[*] Thank you for using Kotosploit! Meow~{Style.RESET_ALL}")
        self.running = False
        sys.exit(0)
    
    def cmd_banner(self, args):
        display_banner()
    
    def cmd_clear(self, args):
        os.system('clear' if os.name != 'nt' else 'cls')
