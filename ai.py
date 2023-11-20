# Version 3.2 - Nov 2023 - J. Hall
# Your openai key should be stored in a file called ".env"
# that is in the same folder as this application.  The content
# of .env needs to be one line that is OPENAI_API_KEY=your key value
#

from openai import OpenAI
import requests
from dotenv import dotenv_values
from pathlib import Path
import base64

STOP = 14
MAX_TOKENS = 500
GPT3_MODEL = "gpt-3.5-turbo-1106"
GPT4_MODEL = "gpt-4-1106-preview"
IMG_MODEL = "dall-e-3"
INSTRUCT_MODEL = "gpt-3.5-turbo-instruct-0914"
VISION_MODEL = "gpt-4-vision-preview"
PP_MODEL = "dalle"
WHISPER_MODEL = "whisper-1"
TTS_MODEL = "tts-1-1106"
TTS_VOICE = "alloy"
TUTOR_TEMP = .2
CHAT_TEMP = .8
FREQ_PENALTY = 1
PRES_PENALTY = 0
TOP_P = .95
SIZE = "1024x1024"

config = dotenv_values(".env")
api_key = config["OPENAI_API_KEY"]
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

# Option 1 - ChatGPT 3.5 Instruct


def instruct():
    prompt = ""
    while True:
        try:
            user_input = input(bold(blue("You: ")))
            prompt += user_input + "\n"
            res = client.completions.create(
                model=INSTRUCT_MODEL,
                prompt=prompt,
                max_tokens=MAX_TOKENS,
                temperature=TUTOR_TEMP,
                stop="",
                top_p=TOP_P,
                presence_penalty=PRES_PENALTY,
                frequency_penalty=FREQ_PENALTY,
            )
            choices_list = res.choices
            first_choice = choices_list[0]
            content = first_choice.text
            print(bold(red("Assistant: ")), content)

        except KeyboardInterrupt:
            print("Exiting...")
            break

# Option 2 - ChatGPT 3.5


def chat3():
    initial_prompt = f"You are a question answering expert. You have a wide range of knowledge and are a world class expert in all things.  When asked questions that require computations, take them one step at a time. If appropriate, give an example to help the user understand your answer."
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

# Option 3 - ChatGPT 4.0


def chat4():
    initial_prompt = f"You are a question answering expert. You have a wide range of knowledge and are a world class expert in all things.  When asked questions that require computations, take them one step at a time. If appropriate, give an example to help the user understand your answer."
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

# Option 4 - Tutor 3.5


def tutor_3():
    initial_input = input(bold(blue("What kind of tutor?: ")))
    initial_prompt = f"You are a world class expert in the field of " + initial_input + \
        ". You will answer the users questions with enough detail that the user will be able to understand how you arrived at the answer.  Your answers can include examples if that will help the user better understand your answer."
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

# Option 5 - Tutor 4


def tutor_4():
    initial_input = input(bold(blue("What kind of tutor?: ")))
    initial_prompt = f"You are a world class expert in the field of " + initial_input + \
        ". You will answer the users questions with enough detail that the user will be able to understand how you arrived at the answer.  Your answers can include examples if that will help the user better understand your answer."
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


# Option 6 - Image Generator


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


# Option 7 - Vision

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def vision():
    image_path = input(bold(blue("Name of image file: ")))
    base64_image = encode_image(image_path)
    text = input(bold(blue("You: ")))
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
    assistant_content = data['choices'][0]['message']['content']
    print(bold(red("Assistant: ")), assistant_content)

# Option 8 - Whisper (Speech to Text)


def whisper():
    choice = input("What is the path/name of the audio file? ")
    audio_file = open(choice, "rb")
    transcript = client.audio.transcriptions.create(WHISPER_MODEL, audio_file)
    print(bold(red("Assistant: ")), transcript["text"])

# Option 9 - TTS (Text to Speech)


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

# Option 10 - List GPT/whisper models


def list_gpt_models():
    print("Current gpt models")
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

# Option 11 - List all models


def list_models():
    print("Current openAI models")
    print("---------------------")
    model_list = client.models.list()
    models_data = model_list.data
    model_ids = [model.id for model in models_data]
    model_ids.sort()
    for id in model_ids:
        print(id)
    input("\nHit Enter to continue . . .")

# Option 12 - List Current Settings


def settings():
    print("\nCurrent Settings:")
    print("-----------------------------------------")
    print("GPT3_MODEL: " + GPT3_MODEL)
    print("GPT4_MODEL: " + GPT4_MODEL)
    print("INSTRUCT_MODEL: " + INSTRUCT_MODEL)
    print("IMG_MODEL: " + IMG_MODEL)
    print("SIZE: " + SIZE)
    print("VISION_MODEL: " + VISION_MODEL)
    print("PP_MODEL: " + PP_MODEL)
    print("WHISPER_MODEL: " + WHISPER_MODEL)
    print("TTS_MODEL: " + TTS_MODEL)
    print("TTS_VOICE: " + TTS_VOICE)
    print("TUTOR_TEMP: " + str(TUTOR_TEMP))
    print("CHAT_TEMP: " + str(CHAT_TEMP))
    print("FREQ_PENALTY: " + str(FREQ_PENALTY))
    print("PRES_PENALTY: " + str(PRES_PENALTY))
    print("TOP_P: " + str(TOP_P))
    print("MAX_TOKENS: " + str(MAX_TOKENS))

    input("\nHit Enter to continue . . .")

# Option 13 - Assistant


def asst():
    thread = client.beta.threads.create()

    while (True):
        try:
            user_input = input(bold(blue("You: ")))

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
                    annotation.text, f' [{index}]')

                # Gather citations based on annotation attributes
                if (file_citation := getattr(annotation, 'file_citation', None)):
                    cited_file = client.files.retrieve(file_citation.file_id)
                    citations.append(
                        f'[{index}] {file_citation.quote} from {cited_file.filename}')
                elif (file_path := getattr(annotation, 'file_path', None)):
                    cited_file = client.files.retrieve(file_path.file_id)
                    citations.append(
                        f'[{index}] Click <here> to download {cited_file.filename}')
                    # Note: File download functionality not implemented above for brevity

            # Add footnotes to the end of the message before displaying to user
            message_content.value += '\n\n' + '\n'.join(citations)
            print(bold(red("Assistant: ")), message_content.value)
        except KeyboardInterrupt:
            print("Exiting...")
            break

# Print Menu


def PrintMenu():
    print("\n")
    print("openAI v3.2 (J. Hall, 2023)")
    print("---------------------------")
    print(" 1 = 3.5 Instruct")
    print(" 2 = 3.5 Chat")
    print(" 3 = 4.0 Chat")
    print(" 4 = 3.5 Tutor")
    print(" 5 = 4.0 Tutor")
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
    PrintMenu()
    try:
        choice = int(input("\nEnter Choice: "))
    except ValueError:
        NotNumeric()
        continue
    if choice == 1:
        instruct()
    elif choice == 2:
        chat3()
    elif choice == 3:
        chat4()
    elif choice == 4:
        tutor_3()
    elif choice == 5:
        tutor_4()
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
        input("\nPlease Make a Choice Between 1 and {0:2d} \nPress <Enter> to return to Main Menu ... "
              .format(STOP))

# Version 1.0   06/07/23     Initial release
# Version 1.1   06/11/23     Added HTML/CSS and Linux options.
# Version 1.2   06/12/23     Added chatGPT4 option.
# Version 1.3   06/20/23     Added Physics tutor.
# Version 1.4   06/21/23     Added Model List and Whisper.
# Version 1.5   07/26/23     Added Church and Law options.
# Version 1.7   08/21/23     Added C and C++ options.
# Version 1.8   08/25/23     Switched to generic tutor function.
# Version 2.0   08/31/23     Added choice of 3.5 or 4 to the tutor function.
# Version 2.1   10/03/23     Added instruct model and broke out model list option.
# Version 3.0   11/07/23     Converted to the updated openai package 1.1.1 which
#                            includes gpt-4-vision
# Version 3.1   11/09/23     Added 'Print Current Settings' option
# Version 3.2   11/12/23     Added the SIU Assistant option
#
