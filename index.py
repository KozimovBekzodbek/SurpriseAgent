import wikipediaapi
import sys
import os
from rich.console import Console
import pyfiglet

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear" )

def print_logo():
    console = Console()
    logo = pyfiglet.figlet_format("Surprise Agent", font="big")
    console.print(f"[bold yellow]{logo}[/bold yellow]")





def save_info_to_txt(query):
    try:
        user_agent = "my-application-name"  # Bu yerga o'zingizning user agent nomingizni kiriting
        wiki = wikipediaapi.Wikipedia(language='uz', user_agent=user_agent)  # O'zbek tilida ma'lumot olish
        page = wiki.page(query)
        
        if not page.exists():
            print(f"{query} haqida ma'lumot topilmadi.")
            return
        
        content = page.text

        # .txt faylga yozish
        with open(f"{query}.txt", "w", encoding="utf-8") as file:
            file.write(content)
        
        print(f"Ma'lumot {query}.txt faylga saqlandi.")
    
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

def main():
    clear_screen()
    print_logo()
    
    query = input("Ma'lumot olishni istagan narsangizni kiriting (masalan, apple): ")
    save_info_to_txt(query)


if __name__ == "__main__":
    main()
