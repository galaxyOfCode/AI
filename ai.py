# Dec 2023 - J. Hall
# Your openai key should be stored in your .bashrc or .zshrc file
# It should contain: export OPENAI_API_KEY="your api key value"
#

import os
import sys
from termcolor import colored, cprint
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from openai import OpenAI

STOP = 14
MAX_TOKENS = 4000
GPT3_MODEL = "gpt-3.5-turbo-1106"
GPT4_MODEL = "gpt-4-1106-preview"
IMG_MODEL = "dall-e-3"
VISION_MODEL = "gpt-4-vision-preview"
WHISPER_MODEL = "whisper-1"
TTS_MODEL = "tts-1-1106"
TTS_VOICE = "alloy"
TUTOR_TEMP = .2
CHAT_TEMP = .8
FREQ_PENALTY = .4
SIZE = "1024x1024"

try:
    api_key = os.environ.get("OPENAI_API_KEY")
except:
    print("No API key found")
client = OpenAI()


def not_numeric():
    """
    Error message if choice is not numeric
    """
    input("\nYou Entered a non-numeric value or wrong format.\nPress <Enter> to continue ... ")
    return

blue1 = colored("You: ", "light_blue", attrs=["bold"])
blue2 = colored("What kind of tutor: ", "light_blue", attrs=["bold"])
blue3 = colored("Select a File: ", "light_blue", attrs=["bold"])
blue4 = colored("Image Description: ", "light_blue", attrs=["bold"])
blue5 = colored("Enter the text: ", "light_blue", attrs=["bold"])
red = colored("Assistant: ", "light_red", attrs=["bold"])

def chat(model):
    """ 
    This is a chatbot for any general subject.  Depending on the calling function it will have a different model but usually the temperature is higher (for a little more creativity).  
    """
    initial_prompt = "You are a question answering expert. You have a wide range of knowledge and are a world class expert in all things.  When asked questions that require computations, take them one step at a time. If appropriate, give an example to help the user understand your answer."
    messages = [{"role": "system", "content": initial_prompt}]
    while True:
        try:
            user_input = input(blue1)
            messages.append({"role": "user", "content": user_input})

            res = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=CHAT_TEMP,
                frequency_penalty=FREQ_PENALTY
            )
            choices_list = res.choices
            first_choice = choices_list[0]
            choice_message = first_choice.message
            content = choice_message.content
            messages.append({"role": "assistant", "content": content})
            print(red, content)
        except KeyboardInterrupt:
            print("Exiting...")
            break


def tutor(model):
    """
    This is a tutor chatbot.  The function will allow the user to input the specific type of tutor.  The calling function determines the model.  The temperature is set lower for less creativity and more factual.
    """
    initial_input = input(blue2)
    initial_prompt = f"You are a world class expert in the field of {initial_input}.You will answer the users questions with enough detail that the user will be able to understand how you arrived at the answer.  Your answers can include examples if that will help the user better understand your answer."
    messages = [{"role": "system", "content": initial_prompt}]
    while True:
        try:
            user_input = input(blue1)
            messages.append({"role": "user", "content": user_input})

            res = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=TUTOR_TEMP,
                frequency_penalty=FREQ_PENALTY
            )

            choices_list = res.choices
            first_choice = choices_list[0]
            choice_message = first_choice.message
            content = choice_message.content
            messages.append({"role": "assistant", "content": content})
            print(red, content)
        except KeyboardInterrupt:
            print("Exiting...")
            break


def code_review(file_path):
    """
    Selects the file for code reviewer
    """
    with open(file_path, "r") as file:
        content = file.read()
    generated_code_review = make_code_review_request(content)
    print(red, generated_code_review)


def make_code_review_request(filecontent):
    """
    Helper function for code reviewer
    """
    initial_prompt = "You will receive a file's contents as text. Generate a code review for the file.  Indicate what changes should be made to improve its style, performance, readability, and maintainability.  If there are any reputable libraries that could be introduced to improve the code, suggest them.  Be kind and constructive.  For each suggested change, include line numbers to which you are referring."
    messages = [
        {"role": "system", "content": initial_prompt},
        {"role": "user", "content": f"Code review the following file: {filecontent}"}
    ]
    res = client.chat.completions.create(
        model=GPT4_MODEL,
        messages=messages
    )
    choices_list = res.choices
    first_choice = choices_list[0]
    choice_message = first_choice.message
    content = choice_message.content
    return content


def code_reviewer():
    """
    Allows the user to select a file for openAI to perform code review
    """
    root = tk.Tk()
    root.withdraw()
    print(blue3)
    file_path = filedialog.askopenfilename(title="Select a File")
    if file_path:
        print(f"Selected file: {file_path}")
        code_review(file_path)
    else:
        print("No file selected or dialog canceled.\n")
        return


def image():
    """
    This will allow the user to input a prompt and openAI will create an image based on the prompt.  IMG_MODEL is the image model that will be used. SIZE is the size of the image.  If IMG_MODEL is not DALL-E-3, then the user can select the number of images, otherwise it will be 1 image.
    """
    prompt = input(blue4)
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
    print(red, image_url)


def encode_image(image_path):
    """
    Helper function for Vision()
    """
    import base64
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except IOError as e:
        print(e)
        return ""


def vision():
    """
    The user can select an image and ask for a description
    """
    import requests
    root = tk.Tk()
    root.withdraw()
    print(blue3)
    image_path = filedialog.askopenfilename(title="Select a File")
    if image_path:
        print(f"Selected file: {image_path}")
    else:
        print("No file selected or dialog canceled.\n")
        return
    base64_image = encode_image(image_path)
    text = input(blue1)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": MAX_TOKENS
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    data = response.json()
    try:
        assistant_content = data["choices"][0]["message"]["content"]
        print(red, assistant_content)
    except:
        error = data["error"]["message"]
        print(red, error)
        return


def whisper():
    """
    This will take an audio file and create and transcribe a text file from the audio source.
    """
    root = tk.Tk()
    root.withdraw()
    print(blue3)
    choice = filedialog.askopenfilename(title="Select a File")
    if choice:
        print(f"Selected file: {choice}")
    else:
        print("No file selected or dialog canceled.\n")
        return
    try:
        with open(choice, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=WHISPER_MODEL, 
                file=audio_file, 
                response_format="text"
            )
            print(red, transcript)
    except IOError as e:
        print(e)
        return


def tts():
    """
    This will take text from a prompt and create an audio file using a specified voice (TTS_VOICE)
    """
    user_input = input(blue5)
    speech_file_path = Path.home().joinpath("Desktop") / "speech.mp3"
    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=user_input
    )
    response.stream_to_file(speech_file_path)
    print(red,
          "'speech.mp3' succesfully created, Check your Desktop\n")


def list_gpt_models():
    """
    List only the GPT models available through the API
    """
    print("Current GPT Models")
    print("------------------")
    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    gpt_model_ids = [
        model_id for model_id in model_ids if model_id.startswith('gpt')]
    gpt_model_ids.sort()
    for id in gpt_model_ids:
        print(id)
    input("\nHit Enter to continue . . .")


def list_models():
    """
    List ALL openAI models available through the API
    """
    print("Current openAI Models")
    print("---------------------")
    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    model_ids.sort()
    for id in model_ids:
        print(id)
    input("\nHit Enter to continue . . .")


def settings():
    """
    Prints off the hardcoded "Magic Numbers"
    """
    print("\nCurrent Settings:")
    print("-----------------------------------")
    print("GPT3_MODEL: " + GPT3_MODEL)
    print("GPT4_MODEL: " + GPT4_MODEL)
    print("IMG_MODEL: " + IMG_MODEL)
    print("SIZE: " + SIZE)
    print("VISION_MODEL: " + VISION_MODEL)
    print("WHISPER_MODEL: " + WHISPER_MODEL)
    print("TTS_MODEL: " + TTS_MODEL)
    print("TTS_VOICE: " + TTS_VOICE)
    print("TUTOR_TEMP: " + str(TUTOR_TEMP))
    print("CHAT_TEMP: " + str(CHAT_TEMP))
    print("FREQ_PENALTY: " + str(FREQ_PENALTY))
    print("MAX_TOKENS: " + str(MAX_TOKENS))

    input("\nHit Enter to continue . . .")


def asst():
    """
    This function implements openAIs Assistant functionality.  I have set up an Assitant along with a file (catalog.pdf).  The intent is that this wil allow the user to ask questions about the SIU catalog.
    """
    thread = client.beta.threads.create()

    while (True):
        try:
            user_input = input(blue1)

            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
            )

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id="asst_tgKa7uBFhwk1lWFn4l42VzNu",
            )

            while (True):
                retrieve = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                if retrieve.status == "completed":
                    messages = client.beta.threads.messages.list(
                        thread_id=thread.id
                    )
                    break

            message_content = messages.data[0].content[0].text
            annotations = message_content.annotations
            citations = []
            for index, annotation in enumerate(annotations):
                # Replace the text with a footnote
                message_content.value = message_content.value.replace(
                    annotation.text, f" [{index}]")

                # Gather citations based on annotation attributes
                if (file_citation := getattr(annotation, "file_citation", None)):
                    cited_file = client.files.retrieve(file_citation.file_id)
                    citations.append(
                        f"[{index}] {file_citation.quote} from {cited_file.filename}")
                elif (file_path := getattr(annotation, "file_path", None)):
                    cited_file = client.files.retrieve(file_path.file_id)
                    citations.append(
                        f"[{index}] Click <here> to download {cited_file.filename}")
                    # Note: File download functionality not implemented above for brevity

            # Add footnotes to the end of the message before displaying to user
            message_content.value += "\n\n" + "\n".join(citations)
            print(red, message_content.value)
        except KeyboardInterrupt:
            print("Exiting...")
            break


def print_menu():
    """
    Prints the main menu
    """
    print("\n")
    print("openAI v3.4.3 (J. Hall, 2023)")
    print("-----------------------------")
    print(" 1 = 3.5 Chat")
    print(" 2 = 4.0 Chat")
    print(" 3 = 3.5 Tutor")
    print(" 4 = 4.0 Tutor")
    print(" 5 = Code Reviewer")
    print(" 6 = Image Generator")
    print(" 7 = Vision")
    print(" 8 = Speech-to-Text")
    print(" 9 = Text-to-Speech")
    print("10 = List GPT Models")
    print("11 = List All Models")
    print("12 = List Current Settings")
    print("13 = SIU Assistant")
    print("14 = Quit")


# Main Loop
while True:
    print_menu()
    try:
        choice = int(input("\nEnter Choice: "))
    except ValueError:
        not_numeric()
        continue
    if choice == 1:
        chat(GPT3_MODEL)
    elif choice == 2:
        chat(GPT4_MODEL)
    elif choice == 3:
        tutor(GPT3_MODEL)
    elif choice == 4:
        tutor(GPT4_MODEL)
    elif choice == 5:
        code_reviewer()
    elif choice == 6:
        image()
    elif choice == 7:
        vision()
    elif choice == 8:
        whisper()
    elif choice == 9:
        tts()
    elif choice == 10:
        list_gpt_models()
    elif choice == 11:
        list_models()
    elif choice == 12:
        settings()
    elif choice == 13:
        asst()
    elif choice == 14:
        quit()
    else:
        input(
            f"\nPlease Make a Choice Between 1 and {STOP} \nPress <Enter> to return to Main Menu ... ")
