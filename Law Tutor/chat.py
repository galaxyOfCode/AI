import openai
import pyperclip
from termcolor import colored

from errors import handle_openai_errors


def chat(client, model, temperature, frequency_penalty, option) -> None:
    """ 
    This is an openAI chatbot.  

    The options are model (gpt-3.5-turbo-1106, etc.);  temperature; freqency_penalty and option
    (1 for general chat and 0 for specific tutoring). All resonses will be displayed and
    copied to the clipboard.
    """
    
    user_prompt = colored("You: ", "light_blue", attrs=["bold"])
    assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])
    try:
        if option:
            initial_prompt = ("You are a question answering expert. You have a wide range "
                              "of knowledge and are a world class expert in all things. "
                              "Give your response in simple terms. If appropriate, give "
                              "an example to help the user understand your answer.")
            messages = [{"role": "system", "content": initial_prompt}]
        else:
            initial_prompt = (f"You are a world class expert in the field of law. "
                              f"You will answer the users questions with enough detail that "
                              f"the user will be able to understand how you arrived at the answer. "
                              f"Your answers can include examples if that will help the user better "
                              f"understand your answer.")
            messages = [{"role": "system", "content": initial_prompt}]
        while True:
            user_input = input(user_prompt)
            messages.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                frequency_penalty=frequency_penalty
            )
            content = response.choices[0].message.content
            print(f"{assistant_prompt} {content}")
            pyperclip.copy(content)
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        print(f"{assistant_prompt} {content}")
        return
    except KeyboardInterrupt:
        print("Exiting...")
        return
