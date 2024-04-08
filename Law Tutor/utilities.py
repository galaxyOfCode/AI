import subprocess
from termcolor import colored


def print_menu():
    """Prints the main menu"""

    menu = """
AI Assistant (J. Hall, 2024)

1 = 4.0 Law Tutor
2 = 3.5 Law Tutor
3 = 4.0 Chat
4 = 3.5 Chat
5 = Image Generator
6 = Speech-to-Text
7 = Text-to-Speech
8 = List Current Settings
9 = Update API
Q = Quit
 """
    print(menu)


def not_numeric() -> None:
    """Error message if menu choice is not numeric"""

    input("\nYou Entered a non-numeric value or wrong format.\nHit <Enter> to continue...")


def list_settings(config) -> None:
    """Prints off the hardcoded "Magic Numbers" """

    print("\nCurrent Settings:\n")
    print(colored("GPT3_MODEL: \t", "blue", attrs=["bold"]), config.GPT3_MODEL)
    print(colored("GPT4_MODEL: \t", "blue", attrs=["bold"]), config.GPT4_MODEL)
    print(colored("IMG_MODEL: \t", "blue", attrs=["bold"]), config.IMG_MODEL)
    print(colored("QUALITY: \t", "blue", attrs=["bold"]), config.QUALITY)
    print(colored("WHISPER_MODEL: \t", "blue",
          attrs=["bold"]), config.WHISPER_MODEL)
    print(colored("TTS_MODEL: \t", "blue", attrs=["bold"]), config.TTS_MODEL)
    print(colored("TTS_VOICE: \t", "blue", attrs=["bold"]), config.TTS_VOICE)
    print(colored("TUTOR_TEMP: \t", "blue", attrs=["bold"]), config.TUTOR_TEMP)
    print(colored("CHAT_TEMP: \t", "blue", attrs=["bold"]), config.CHAT_TEMP)
    print(colored("FREQ_PENALTY: \t", "blue",
          attrs=["bold"]), config.FREQ_PENALTY)
    print(colored("MAX_TOKENS: \t", "blue", attrs=["bold"]), config.MAX_TOKENS)
    input("\nHit <Enter> to continue...")


def update() -> None:
    """Updates the 'openai' package"""

    package = "openai"
    original_version = check_package_version(package)
    subprocess.check_call(["pip", "install", "--upgrade",
                          "openai"], stdout=subprocess.DEVNULL)
    updated_version = check_package_version(package)
    if original_version == "error" or updated_version == "error":
        return
    if original_version != updated_version:
        print(f"\nOpenAI updated to version {updated_version}\n")
    else:
        print(f"\nOpenAI is already up to date ({original_version})\n")
    input("Hit <Enter> to continue...")


def check_package_version(package_name):
    """Returns the version number of a python package"""

    try:
        result = subprocess.check_output(
            ["pip", "show", package_name], stderr=subprocess.DEVNULL).decode("utf-8")
        for line in result.split("\n"):
            if line.startswith("Version:"):
                return line.split(": ")[1]
    except subprocess.CalledProcessError:
        print(f"\n{package_name} package not found\n")
        return "error"
