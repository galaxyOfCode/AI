import openai
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live

from errors import handle_openai_errors


def chat(client, model, temperature, frequency_penalty, option, console: Console) -> None:
    """ 
    Communicates with OpenAI's chatbot using Rich for a polished UI.
    """
    
    if option:
        initial_prompt = ("You are a pragmatic, matter-of-fact assistant. Your goal is to provide accurate information with maximum density and minimum word count. Avoid conversational filler, polite transitions (e.g., 'I hope this helps,' 'Certainly!'), and flowery adjectives. Do not offer unsolicited opinions or moral guidance unless it is a direct technical requirement of the query. If a question is objective, provide an objective answer. If information is missing, state that it is missing without apology. Be brief, clinical, and direct.")
    else:
        initial_prompt = ("You are a senior legal assistant. Your communication style is clinical, precise, and devoid of emotional or conversational filler. Prioritize legal accuracy and structural clarity. Use 'shall' and 'may' strictly according to their legal definitions. Avoid introductory pleasantries (e.g., 'I hope this helps,' 'I have drafted...'). If a legal standard is requested, cite the relevant code or principle directly. If a facts-based query is ambiguous, state 'Insufficient data' rather than speculating. Responses should be formatted with clear headings or numbered lists to maximize scannability. Do not offer personal opinions; provide only objective legal information and drafting assistance. If you cite a specific law or case, double check to ensure it is correct.")

    messages = [{"role": "system", "content": initial_prompt}]

    try:
        while True:
            console.print("\n[bold bright_blue]You:[/bold bright_blue]", end=" ")
            user_input = input()
            
            if user_input.lower() in ["exit", "quit", "q"]:
                break

            messages.append({"role": "user", "content": user_input})

            with console.status("[bold bright_red]Assistant is thinking...[/bold bright_red]", spinner="dots"):
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    frequency_penalty=frequency_penalty
                )
            
            content = response.choices[0].message.content
            
            console.print(
                Panel(
                    Markdown(content),
                    title="[bold bright_red]Assistant[/bold bright_red]",
                    title_align="left",
                    border_style="bright_red"
                )
            )

            messages.append({"role": "assistant", "content": content})
            pyperclip.copy(content)

    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        handle_openai_errors(e)
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting...[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Something went wrong:[/bold red] {e}")
