from colorama import Fore, Style


def clear_text_from_ansi(text):
    return (
        text.replace(Fore.RED, "")
        .replace(Fore.GREEN, "")
        .replace(Fore.YELLOW, "")
        .replace(Fore.BLUE, "")
        .replace(Style.RESET_ALL, "")
    )


def color_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"


def text_percentage(percentage):
    if percentage > 55:
        return color_text(f"(~{percentage:.2f}%)", Fore.GREEN)
    if percentage > 49 and percentage < 56:
        return color_text(f"(~{percentage:.2f}%)", Fore.YELLOW)
    return color_text(f"(~{percentage:.2f}%)", Fore.RED)


def print_with_blank_line_in_front(text):
    print()
    print(text)
