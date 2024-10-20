import sys
import os
import asyncio
from core.browser_manager import handle_interactive_session, close_browser
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    """Displays the help menu with available commands."""
    print(f"\n{Fore.CYAN}=== Spectre Command Centre Help ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}help{Style.RESET_ALL}     - Show this help menu")
    print(f"{Fore.GREEN}options{Style.RESET_ALL}  - Show available options")
    print(f"{Fore.GREEN}start{Style.RESET_ALL}    - Start a new interactive session")
    print(f"{Fore.GREEN}exit{Style.RESET_ALL}     - Exit the program")
    print(f"{Fore.CYAN}==================================={Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}In the interactive session:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}navigate{Style.RESET_ALL} - Navigate to a new URL")
    print(f"{Fore.GREEN}extract{Style.RESET_ALL}  - Extract links from the current page")
    print(f"{Fore.GREEN}exit{Style.RESET_ALL}     - Exit the interactive session")
    print()

def show_options():
    """Displays the available options."""
    print(f"\n{Fore.CYAN}=== Spectre Command Centre Options ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Start a New Interactive Session{Style.RESET_ALL}")
    print(f"{Fore.RED}2. Exit{Style.RESET_ALL}")
    print(f"{Fore.CYAN}====================================={Style.RESET_ALL}\n")

async def main():
    """Main function to run the command centre interface."""
    try:
        clear_screen()
        print(f"{Fore.CYAN}Welcome to Spectre Command Centre{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type 'help' for available commands{Style.RESET_ALL}")

        while True:
            command = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip().lower()
            
            if command == 'help':
                show_help()
            elif command == 'options':
                show_options()
            elif command == 'start':
                url = input(f"{Fore.YELLOW}Enter the URL to navigate to: {Style.RESET_ALL}")
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                print(f"{Fore.MAGENTA}Starting interactive session...{Style.RESET_ALL}")
                await handle_interactive_session(url, headless=False)
                clear_screen()
            elif command == 'exit':
                print(f"{Fore.RED}Exiting Spectre Command Centre. Goodbye!{Style.RESET_ALL}")
                break
            elif command == 'clear':
                clear_screen()
            else:
                print(f"{Fore.RED}Invalid command. Type 'help' for available commands.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
    finally:
        # No need to explicitly close browser and playwright here
        pass

if __name__ == "__main__":
    asyncio.run(main())
