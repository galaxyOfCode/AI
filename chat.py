from termcolor import colored
import configparser
import pyperclip

cfg = configparser.ConfigParser()
cfg.read('config.ini')
FREQ_PENALTY = cfg.getfloat('PARAM', 'FREQ_PENALTY')
CHAT_TEMP = cfg.getfloat('PARAM', 'CHAT_TEMP')
TUTOR_TEMP = cfg.getfloat('PARAM', 'TUTOR_TEMP')

blue1 = colored("You: ", "light_blue", attrs=["bold"])
blue2 = colored("What kind of tutor: ", "light_blue", attrs=["bold"])
red = colored("Assistant: ", "light_red", attrs=["bold"])


def chat(model, client):
    ''' 
    This is a chatbot for any general subject.  Depending on the calling function it will have a different model but usually the temperature is higher (for a little more creativity).  
    '''
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
            content = res.choices[0].message.content
            print(red, content)
            pyperclip.copy(content)
        except KeyboardInterrupt:
            print("Exiting...")
            break


def tutor(model, client):
    '''
    This is a tutor chatbot.  The function will allow the user to input the specific type of tutor.  The calling function determines the model.  The temperature is set lower for less creativity and more factual.
    '''
    initial_input = input(blue2)
    initial_prompt = f"You are a world class expert in the field of {initial_input}. You will answer the users questions with enough detail that the user will be able to understand how you arrived at the answer.  Your answers can include examples if that will help the user better understand your answer."
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
            content = res.choices[0].message.content
            print(red, content)
            pyperclip.copy(content)
        except KeyboardInterrupt:
            print("Exiting...")
            break
