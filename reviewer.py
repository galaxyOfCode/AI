import openai
import os
import pyperclip
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

from errors import handle_openai_errors, handle_file_errors
from PyPDF2 import PdfReader

console = Console()

def extract_text_from_file(file_path) -> str:
    """Extracts text from a file. Supports both text files and PDFs."""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    _, ext = os.path.splitext(file_path).lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    elif ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            return "".join([page.extract_text() for page in reader.pages])
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {e}")
    else:
        raise ValueError("Unsupported file type. Please provide a .txt or .pdf file.")

def doc_review(client, model) -> None:
    """Reviews a document and allows for a continuous follow-up conversation."""

    try:
        file_path = Prompt.ask("[bold bright_green]Enter the path to your file[/bold bright_green] (.txt or .pdf)")
        
        if not file_path or not os.path.exists(file_path):
            console.print("[yellow]Invalid file path.[/yellow]")
            return

        try:
            with console.status("[bold green]Extracting text...[/bold green]"):
                file_content = extract_text_from_file(file_path)
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            return

        system_instruction = (
            "You will receive a document. Please review the document and provide answers to the user's prompt based on the contents of the document. If it will help the user, please provide references to page numbers."
        )
        
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "system", "content": f"DOCUMENT CONTENT:\n{file_content}"}
        ]

        console.print("[italic]Chat started! Type 'quit' or 'q' to stop.[/italic]\n")

        while True:
            user_input = Prompt.ask("[bold bright_blue]You[/bold bright_blue]")

            if user_input.lower() in ["exit", "quit" "q"]:
                break

            messages.append({"role": "user", "content": user_input})

            try:
                with console.status("[bold red]Assistant is thinking..."):
                    response = client.chat.completions.create(
                        model=model,
                        messages=messages
                    )
                    content = response.choices[0].message.content
                
                messages.append({"role": "assistant", "content": content})

                console.print("\n")
                console.print(Panel(Markdown(content), title="[bold red]Assistant[/bold red]", border_style="red"))
                
                pyperclip.copy(content)
                console.print("[italic cyan]Response copied to clipboard![/italic cyan]\n")

            except (openai.APIConnectionError, openai.RateLimitError, openai.APIStatusError) as e:
                content = handle_openai_errors(e)
                console.print(Panel(content, title="[bold red]API Error[/bold red]", expand=False))
                break 

    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
    
    console.print("[yellow]Exiting document review...[/yellow]")
