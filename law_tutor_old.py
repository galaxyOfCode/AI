# Version 1.0 - Jun 2023 - J. Hall
# Your openai key should be stored in a file called ".env"
# that is in the same folder as this application.  The content
# needs to be one line that is OPENAI_API_KEY=your key value
#

import openai
from dotenv import dotenv_values

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

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

def chat():
    initial_prompt = f"You are a law school tutor helping students prepare for the bar exam. Your personality is helpful and freindly"
    messages = [{"role": "system", "content": initial_prompt}]

    while True:
        try:
            user_input = input(bold(blue("You: ")))
            messages.append({"role": "user", "content": user_input})

            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )  

            messages.append(res["choices"][0]["message"].to_dict())
            print(bold(red("Assistant: ")),res["choices"][0]["message"]["content"])

        except KeyboardInterrupt:
            print("Exiting...")
            break

    print(res)

chat()

# Version 1.0     6/7/23      Initial release
#