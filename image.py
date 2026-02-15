import base64
import openai
from pathlib import Path
import pyperclip
import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.status import Status

from errors import (handle_request_errors,
                    handle_openai_errors,
                    handle_file_errors)


console = Console()

def generate_image(client, model, quality) -> None:
    prompt_text = Prompt.ask("[bold bright_blue]Image Description[/bold bright_blue]")

    if not prompt_text:
        return

    try:
        with Status("[bold green]Generating image...", spinner="aesthetic") as status:
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
        
    except Exception as e:
        console.print(f"\n[bold red]Unexpected Error:[/bold red] {e}")
        console.input("\n[yellow]Press Enter to acknowledge error...[/yellow]")


def describe_image(api_key, model, max_tokens) -> None:
    """The user provides an image path and asks for a description using Rich UI."""

    prompt_text = Prompt.ask("[bold bright_blue]You[/bold bright_blue]")

    image_path = Prompt.ask("[bold bright_blue]Enter image file path[/bold bright_blue]")

    if not image_path:
        console.print("[yellow]No file path provided. Operation cancelled.[/yellow]\n")
        return

    with Status("[bold green]Processing image...[/bold green]", spinner="dots") as status:
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        except (PermissionError, OSError, FileNotFoundError) as e:
            content = handle_file_errors(e)
            console.print(Panel(content, title="File Error", border_style="red"))
            return

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": model,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }], 
            "max_tokens": max_tokens
        }

        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
            )
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            content = handle_request_errors(e)
            console.print(f"\n[bold bright_red]Assistant:[/bold bright_red] {content}")
            Prompt.ask("\nPress [bold]Enter[/bold] to continue")
            return

    try:
        content = data["choices"][0]["message"]["content"]
        
        console.print("\n[bold bright_red]Assistant:[/bold bright_red]")
        console.print(Panel(content, border_style="bright_red"))
        
        pyperclip.copy(content)
        console.print("[italic green](Description copied to clipboard)[/italic green]")
        console.input("\nPress [bold]Enter[/bold] to continue...")
        
    except Exception as e:
        error_msg = data.get("error", {}).get("message", str(e))
        console.print(f"[bold red]Something went wrong:[/bold red] {error_msg}")
        console.input("\n[yellow]Press Enter to acknowledge error...[/yellow]")
