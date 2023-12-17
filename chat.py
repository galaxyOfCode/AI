import openai
import pyperclip
from termcolor import colored

user_prompt = colored("You: ", "light_blue", attrs=["bold"])
tutor_prompt = colored("What kind of tutor: ", "light_blue", attrs=["bold"])
assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])


def chat(client, model, temperature, frequency_penalty, option):
    ''' 
    This is an openai chatbot.  
    
    The options are model (gpt-3.5-turbo-1106, etc);  temperature; freqency_penalty
    and option (1 for general chat and 0 for specific tutoring). All resonses will be displayed and copied to the clipboard.
    '''
    try:
        if option:
            initial_prompt = "You are a question answering expert. You have a wide range of knowledge and are a world class expert in all things.  When asked questions that require computations, take them one step at a time. If appropriate, give an example to help the user understand your answer."
            messages = [{"role": "system", "content": initial_prompt}]
        else:
            initial_input = input(tutor_prompt)
            initial_prompt = f"You are a world class expert in the field of {initial_input}. You will answer the users questions with enough detail that the user will be able to understand how you arrived at the answer.  Your answers can include examples if that will help the user better understand your answer."
            messages = [{"role": "system", "content": initial_prompt}]
        while True:
            user_input = input(user_prompt)
            messages.append({"role": "user", "content": user_input})

            res = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                frequency_penalty=frequency_penalty
            )
            content = res.choices[0].message.content
            print(f"{assistant_prompt} {content}")
            pyperclip.copy(content)
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)
        return
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        return
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        return
    except KeyboardInterrupt:
        print("Exiting...")
        return
