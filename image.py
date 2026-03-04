"""Generates and describes images using OpenAI's image generation and chat models, with error handling for API and file-related issues."""

import base64
from pathlib import Path
import openai
import pyperclip
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.status import Status

from errors import (handle_openai_errors,
                    handle_file_errors)


def generate_image(client: openai.OpenAI, model: str, console: Console) -> None:
    """Generates an image based on user input and saves it to the desktop using OpenAI's image generation capabilities."""

    prompt_text = Prompt.ask("[bold bright_blue]Image Description[/bold bright_blue]")

    if not prompt_text:
        return

    try:
        with Status("[bold green]Generating image...", spinner="aesthetic"):
            img = client.images.generate(
                model=model,
                prompt=prompt_text,
                n=1,
                size="1024x1024"
            )

            desktop_path = Path.home() / "Desktop" / "output.png"

            image_bytes = base64.b64decode(img.data[0].b64_json)
            with open(desktop_path, "wb") as f:
                f.write(image_bytes)

        console.print("\n")
        console.print(Panel(
            f"[bold green]Success![/bold green]\n\nImage saved to: [cyan]{desktop_path}[/cyan]",
            title="Assistant",
            border_style="bright_blue",
            expand=False
        ))

        console.input("\nPress [bold]Enter[/bold] to return to menu...")

    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        error_content = handle_openai_errors(e)
        console.print(Panel(f"[bold red]API Error:[/bold red]\n{error_content}", border_style="red"))
        console.input("\n[yellow]Press Enter to acknowledge error...[/yellow]")

    except (IOError, OSError, ValueError) as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        console.input("\n[yellow]Press Enter to acknowledge error...[/yellow]")


def describe_image(client: openai.OpenAI, model: str, max_tokens: int, console: Console) -> None:
    """Describes an image based on user input and the image file provided, using OpenAI's chat model with image input capabilities."""

    prompt_text = Prompt.ask("[bold bright_blue]You[/bold bright_blue]")
    image_path = Prompt.ask("[bold bright_blue]Enter image file path[/bold bright_blue]")

    if not image_path or not Path(image_path).exists():
        console.print("[yellow]Invalid path or file missing.[/yellow]")
        return

    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    except (IOError, OSError) as e:
        console.print(Panel(handle_file_errors(e), title="File Error", border_style="red"))
        return

    try:
        with console.status("[bold green]Analyzing image...[/bold green]", spinner="dots"):
            response = client.chat.completions.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                        }
                    ]
                }],
                max_tokens=max_tokens
            )
        content = response.choices[0].message.content

        console.print("\n[bold bright_red]Assistant:[/bold bright_red]")
        console.print(Panel(content, border_style="bright_red"))
        pyperclip.copy(content)
        console.print("[italic green](Copied to clipboard)[/italic green]")
        console.input("\nPress [bold]Enter[/bold] to continue...")

    except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
        console.print(Panel(handle_openai_errors(e), title="API Error", border_style="red"))
    except (ValueError, KeyError) as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        