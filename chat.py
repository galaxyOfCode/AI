import openai
import pyperclip
from termcolor import colored

from errors import handle_openai_errors


def chat(client, model, temperature, frequency_penalty, option) -> None:
    """ 
    Communicates with OpenAI's chatbot to generate responses based on user input.

    Parameters:
    - client: The OpenAI client instance.
    - model: The model used for generating responses (e.g., 'gpt-4o').
    - temperature: Controls randomness in the response.
    - frequency_penalty: Decreases the likelihood of repetition in responses.
    - option: Determines if it's a general chat (1) or law tutoring (0).
    """

    user_prompt = colored("You: ", "light_blue", attrs=["bold"])
    assistant_prompt = colored("Assistant: ", "light_red", attrs=["bold"])
    try:
        if option:
            initial_prompt = ("""You are a helpful and friendly question answering expert. You can call the user by her first name, which is Ellen.  You have a wide range of knowledge and are a world class expert in all things. Give your response in simple terms. If appropriate, give an example to help the user understand your answer.""")
            messages = [{"role": "system", "content": initial_prompt}]
        else:
            initial_prompt = (f"""You are a helpful and friendly law expert. The user is a new lawyer specializing in immigration law and will need expert advice.  You will answer the users questions with enough detail that the user will be able to understand how you arrived at the answer. Your answers can include examples if that will help the user better understand your answer.  If you give citations, make sure you check that they are correct.  You can call the user by her first name, which is Ellen.""")
            messages = [{"role": "system", "content": initial_prompt}]
        while True:
            user_input = input(user_prompt)
            messages.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                frequency_penalty=frequency_penalty)
            content = response.choices[0].message.content
            print(f"{assistant_prompt} {content}")
            messages.append({"role": "assistant", "content": content})
            pyperclip.copy(content)
    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        content = handle_openai_errors(e)
        print(f"{assistant_prompt} {content}")
        return
    except KeyboardInterrupt:
        print("Exiting...")
        return
    except Exception as e:
        print(f"{assistant_prompt} Something went wrong: {e}")
