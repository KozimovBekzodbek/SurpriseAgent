import wikipediaapi
import os
import re
import textwrap
import logging
from rich.console import Console
from rich.prompt import Prompt
import pyfiglet

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

console = Console()

LANGUAGES = {
    "1": ("uz", "O'zbekcha"),
    "2": ("ru", "Русский"),
    "3": ("en", "English"),
    "4": ("ar", "العربية")
}

translations = {
    "uz": {
        "choose_lang": "Tilni tanlang:",
        "search_prompt": "Qidiruv uchun mavzuni kiriting",
        "not_found": " haqida ma'lumot topilmadi.",
        "saved": "Ma'lumot saqlandi:"
    },
    "ru": {
        "choose_lang": "Выберите язык:",
        "search_prompt": "Введите тему для поиска",
        "not_found": " информация не найдена.",
        "saved": "Информация сохранена:"
    },
    "en": {
        "choose_lang": "Choose a language:",
        "search_prompt": "Enter a topic to search",
        "not_found": " not found.",
        "saved": "Information saved:"
    },
    "ar": {
        "choose_lang": "اختر اللغة:",
        "search_prompt": "أدخل موضوع البحث",
        "not_found": " لم يتم العثور على معلومات عنه.",
        "saved": "تم حفظ المعلومات:"
    }
}

def clear_screen() -> None:

    os.system("cls" if os.name == "nt" else "clear")





def print_logo() -> None:

    logo = pyfiglet.figlet_format("Surprise Agent", font="big")
    console.print(f"[bold yellow]{logo}[/bold yellow]")




def sanitize_filename(filename: str) -> str:

    return re.sub(r'[\/:*?"<>|]', '_', filename)




def format_text(text: str, width: int = 100) -> str:

    paragraphs = text.split("\n")
    formatted_text = "\n\n".join("\n".join(textwrap.wrap(paragraph, width)) for paragraph in paragraphs if paragraph.strip())

    return formatted_text




def save_info_to_txt(query: str, lang: str) -> None:

    try:

        wiki = wikipediaapi.Wikipedia(language=lang, user_agent="SurpriseAgent/1.0")
        page = wiki.page(query)

        if not page.exists():
            console.print(f"[bold red]{query} {translations[lang]['not_found']}[/bold red]")

            return

        filename = sanitize_filename(query) + f"_{lang}.txt"

        formatted_content = f"{page.title}\n" + "=" * len(page.title) + "\n\n"

        formatted_content += format_text(page.text)


        with open(filename, "w", encoding="utf-8") as file:
            file.write(formatted_content)

        console.print(f"[bold green]{translations[lang]['saved']} {filename}.[/bold green]")


    except Exception as e:

        logging.error(f"Error occurred: {e}")
        console.print(f"[bold red]An error occurred while fetching data.[/bold red]")





def choose_language() -> str:

    console.print("\n".join([f"[bold cyan]{k}[/bold cyan] - {v[1]}" for k, v in LANGUAGES.items()]))
    
    while True:
        lang_choice = Prompt.ask("[bold cyan]Tilni tanlang / Выберите язык / Choose a language / اختر اللغة[/bold cyan]", choices=LANGUAGES.keys())
        lang_code = LANGUAGES[lang_choice][0]

        return lang_code





def main() -> None:

    clear_screen()
    print_logo()

    lang = choose_language()
    query = Prompt.ask(f"[bold cyan]{translations[lang]['search_prompt']}[/bold cyan]")

    save_info_to_txt(query, lang)

if __name__ == "__main__":
    main()

