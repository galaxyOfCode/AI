from termcolor import colored
import pyperclip

blue1 = colored("You: ", "light_blue", attrs=["bold"])
red = colored("Assistant: ", "light_red", attrs=["bold"])


def siu_assistant(client):
    '''
    This function implements openAIs Assistant functionality.  I have set up an Assitant along with a file (catalog.pdf).  The intent is that this wil allow the user to ask questions about the SIU catalog.
    '''
    thread = client.beta.threads.create()

    while (True):
        try:
            user_input = input(blue1)

            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input)

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id="asst_tgKa7uBFhwk1lWFn4l42VzNu",)

            while (True):
                retrieve = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id)
                if retrieve.status == "completed":
                    messages = client.beta.threads.messages.list(
                        thread_id=thread.id)
                    break

            message_content = messages.data[0].content[0].text
            annotations = message_content.annotations
            citations = []
            for index, annotation in enumerate(annotations):
                # Replace the text with a footnote
                message_content.value = message_content.value.replace(
                    annotation.text, f" [{index}]")

                # Gather citations based on annotation attributes
                if (file_citation := getattr(annotation, "file_citation", None)):
                    cited_file = client.files.retrieve(file_citation.file_id)
                    citations.append(
                        f"[{index}] {file_citation.quote} from {cited_file.filename}")
                elif (file_path := getattr(annotation, "file_path", None)):
                    cited_file = client.files.retrieve(file_path.file_id)
                    citations.append(
                        f"[{index}] Click <here> to download {cited_file.filename}")
                    # Note: File download functionality not implemented above for brevity

            # Add footnotes to the end of the message before displaying to user
            message_content.value += "\n\n" + "\n".join(citations)
            print(red, message_content.value)
            pyperclip.copy(message_content.value)
        except KeyboardInterrupt:
            print("Exiting...")
            break
