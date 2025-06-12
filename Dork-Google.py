#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import argparse
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

class GoogleDorkScanner:
    def __init__(self):
        self.base_url = 'https://www.exploit-db.com/google-hacking-database'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.results = []

    def fetch_dorks(self, category=None, author=None):
        try:
            print(f"{Fore.CYAN}[*] Fetching Google Dorks from Exploit-DB...{Style.RESET_ALL}")
            
            response = requests.get(self.base_url, headers=self.headers)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: HTTP {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            dork_table = soup.find('table', {'id': 'exploits-table'})
            
            if not dork_table:
                raise Exception("Could not find dorks table on the page")

            for row in dork_table.find_all('tr')[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 4:
                    dork_data = {
                        'date': cols[0].text.strip(),
                        'dork': cols[1].text.strip(),
                        'category': cols[2].text.strip(),
                        'author': cols[3].text.strip()
                    }

                    # Apply filters if specified
                    if category and category.lower() not in dork_data['category'].lower():
                        continue
                    if author and author.lower() not in dork_data['author'].lower():
                        continue

                    self.results.append(dork_data)
                    self._print_dork(dork_data)

        except Exception as e:
            print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")

    def _print_dork(self, dork):
        print(f"\n{Fore.GREEN}[+] Found Dork:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Date:{Style.RESET_ALL} {dork['date']}")
        print(f"{Fore.YELLOW}Dork:{Style.RESET_ALL} {dork['dork']}")
        print(f"{Fore.YELLOW}Category:{Style.RESET_ALL} {dork['category']}")
        print(f"{Fore.YELLOW}Author:{Style.RESET_ALL} {dork['author']}")
        print("-" * 80)

    def save_results(self):
        if not self.results:
            print(f"\n{Fore.RED}[!] No results to save{Style.RESET_ALL}")
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"google_dorks_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': timestamp,
                    'total_dorks': len(self.results),
                    'dorks': self.results
                }, f, indent=4, ensure_ascii=False)

            print(f"\n{Fore.GREEN}[+] Results saved to: {filename}{Style.RESET_ALL}")

        except Exception as e:
            print(f"\n{Fore.RED}[!] Error saving results: {str(e)}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(
        description='Google Dorks Scanner - Fetch dorks from Exploit-DB GHDB',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-c', '--category', help='Filter dorks by category')
    parser.add_argument('-a', '--author', help='Filter dorks by author')
    args = parser.parse_args()

    scanner = GoogleDorkScanner()
    scanner.fetch_dorks(category=args.category, author=args.author)
    scanner.save_results()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Search interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] An error occurred: {str(e)}{Style.RESET_ALL}")