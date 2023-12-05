# Law Tutor Version 2.0 - Dec 2023 - J. Hall
# Your openai key should be stored in your .bashrc or .zshrc file
# It should contain: export OPENAI_API_KEY="your api key value"
#

from openai import OpenAI
import os
from pathlib import Path

STOP = 7
MAX_TOKENS = 5000
GPT3_MODEL = "gpt-3.5-turbo-1106"
GPT4_MODEL = "gpt-4-1106-preview"
IMG_MODEL = "dall-e-3"
TTS_MODEL = "tts-1-1106"
TTS_VOICE = "nova"
TUTOR_TEMP = .2
CHAT_TEMP = .8
FREQ_PENALTY = 1
PRES_PENALTY = 0
TOP_P = .95
SIZE = "1024x1024"

api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI()


def NotNumeric():
    input("\nYou Entered a non-numeric value or wrong format.\nPress <Enter> to continue ... ")
    return


def bold(text):
    bold_start = "\033[1m"
    bold_end = "\033[0m"
    return bold_start + text + bold_end


def blue(text):
    blue_start = "\033[34m"
    blue_end = "\033[0m"
    return blue_start + text + blue_end


def red(text):
    red_start = "\033[31m"
    red_end = "\033[0m"
    return red_start + text + red_end


# Option 1 - Law Tutor 4.0


def law4():
    initial_prompt = "You are a law school tutor. Your knowledge of law school subjects is extensive.  Answer in terms appropriate for a first year law school student. If appropriate, give an example to help the user understand your answer."
    messages = [{"role": "system", "content": initial_prompt}]

    while True:
        try:
            user_input = input(bold(blue("You: ")))
            messages.append({"role": "user", "content": user_input})

            res = client.chat.completions.create(
                model=GPT4_MODEL,
                messages=messages,
                temperature=TUTOR_TEMP,
                frequency_penalty=FREQ_PENALTY
            )

            choices_list = res.choices
            first_choice = choices_list[0]
            choice_message = first_choice.message
            content = choice_message.content
            messages.append({"role": "assistant", "content": content})
            print(bold(red("Assistant: ")), content)

        except KeyboardInterrupt:
            print("Exiting...")
            break

# Option 2 - chatbot 4.0


def chat4():
    initial_prompt = "You are a question answering expert. You have a wide range of knowledge and are a world class expert in all things.  When asked questions that require computations, take them one step at a time. If appropriate, give an example to help the user understand your answer."
    messages = [{"role": "system", "content": initial_prompt}]

    while True:
        try:
            user_input = input(bold(blue("You: ")))
            messages.append({"role": "user", "content": user_input})

            res = client.chat.completions.create(
                model=GPT4_MODEL,
                messages=messages,
                temperature=CHAT_TEMP,
                frequency_penalty=FREQ_PENALTY
            )

            choices_list = res.choices
            first_choice = choices_list[0]
            choice_message = first_choice.message
            content = choice_message.content
            messages.append({"role": "assistant", "content": content})
            print(bold(red("Assistant: ")), content)

        except KeyboardInterrupt:
            print("Exiting...")
            break

# Option 3 - Law Tutor 3.5


def law3():
    initial_prompt = "You are a law school tutor. Your knowledge of law school subjects is extensive.  Answer in terms appropriate for a first year law school student. If appropriate, give an example to help the user understand your answer."
    messages = [{"role": "system", "content": initial_prompt}]

    while True:
        try:
            user_input = input(bold(blue("You: ")))
            messages.append({"role": "user", "content": user_input})

            res = client.chat.completions.create(
                model=GPT3_MODEL,
                messages=messages,
                temperature=TUTOR_TEMP,
                frequency_penalty=FREQ_PENALTY
            )

            choices_list = res.choices
            first_choice = choices_list[0]
            choice_message = first_choice.message
            content = choice_message.content
            messages.append({"role": "assistant", "content": content})
            print(bold(red("Assistant: ")), content)

        except KeyboardInterrupt:
            print("Exiting...")
            break

# Option 4 - chatbot 3.5


def chat3():
    initial_prompt = "You are a question answering expert. You have a wide range of knowledge and are a world class expert in all things.  When asked questions that require computations, take them one step at a time. If appropriate, give an example to help the user understand your answer."
    messages = [{"role": "system", "content": initial_prompt}]

    while True:
        try:
            user_input = input(bold(blue("You: ")))
            messages.append({"role": "user", "content": user_input})

            res = client.chat.completions.create(
                model=GPT3_MODEL,
                messages=messages,
                temperature=CHAT_TEMP,
                frequency_penalty=FREQ_PENALTY
            )

            choices_list = res.choices
            first_choice = choices_list[0]
            choice_message = first_choice.message
            content = choice_message.content
            messages.append({"role": "assistant", "content": content})
            print(bold(red("Assistant: ")), content)

        except KeyboardInterrupt:
            print("Exiting...")
            break

# Option 5 - Image Generator


def image():
    prompt = input(bold(blue("Image Desc: ")))
    if (IMG_MODEL != "dall-e-3"):
        n = int(input("\nNumber of Images: "))
    else:
        choice = int(
            input("\nQuality - Enter 1 for 'HD' or 2 for 'Standard': "))
        if (input == 1):
            quality = "hd"
        else:
            quality = "standard"
        n = 1
    if (choice == 1):
        res = client.images.generate(
            model=IMG_MODEL,
            prompt=prompt,
            size=SIZE,
            quality=quality,
            n=n,
        )
    else:
        res = client.images.generate(
            model=IMG_MODEL,
            prompt=prompt,
            size=SIZE,
            n=n
        )

    images_data = res.data
    first_image = images_data[0]
    image_url = first_image.url
    print(bold(red("Assistant: ")), image_url)


# Option 6 - Text to Speech


def tts():
    choice = input(bold(blue("Enter the text: ")))
    speech_file_path = Path.home().joinpath("Desktop") / "speech.mp3"
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=choice
    )
    response.stream_to_file(speech_file_path)
    print(bold(red("Assistant: ")), "Check your Desktop for 'speech.mp3'")


# Print Menu


def PrintMenu():
    print("\n")
    print("Law Tutor v2.0 (J. Hall, 2023)")
    print("------------------------------")
    print(" 1 = Law Tutor")
    print(" 2 = 4.0 Chat")
    print(" 3 = Law Tutor (3.5)")
    print(" 4 = 3.5 Chat")
    print(" 5 = Image Generator")
    print(" 6 = Text-to-Speech")
    print(" 7 = Quit")


# Main Loop
while True:
    PrintMenu()
    try:
        choice = int(input("\nEnter Choice: "))
    except ValueError:
        NotNumeric()
        continue
    if choice == 1:
        law4()
    elif choice == 2:
        chat4()
    elif choice == 3:
        law3()
    elif choice == 4:
        chat3()
    elif choice == 5:
        image()
    elif choice == 6:
        tts()
    elif choice == 7:
        quit()
    else:
        input("\nPlease Make a Choice Between 1 and {0:2d} \nPress <Enter> to return to Main Menu ... "
              .format(STOP))

# Version 1.0   06/07/23     Initial release
# Version 2.0   12/01/23     Updated to be consistent with ai.py ver 3.4
#
