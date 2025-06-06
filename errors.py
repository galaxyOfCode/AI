import openai
from requests.exceptions import HTTPError, Timeout, RequestException


def handle_file_errors(exception) -> str:
    if isinstance(exception, FileNotFoundError):
        return "Error: The file was not found."
    elif isinstance(exception, PermissionError):
        return "Error: Permission denied when trying to read the file."
    elif isinstance(exception, OSError):
        return "Error: An error occurred while reading from the file."
    return "An unknown file error occurred."


def handle_openai_errors(exception) -> str:
    if isinstance(exception, openai.APIConnectionError):
        return "The server could not be reached\n" + \
            str(exception.__cause__)
    elif isinstance(exception, openai.RateLimitError):
        return "A 'Rate Limit Notice' was received; we should back off a bit."
    elif isinstance(exception, openai.APIStatusError):
        return "A non-200-range status code was received: " + \
            str(exception.status_code) + " " + str(exception.response)
    return "An unknown openAI error occurred."


def handle_request_errors(exception) -> str:
    if isinstance(exception, HTTPError):
        return "An HTTP error occurred"
    elif isinstance(exception, Timeout):
        return "The request timed-out"
    elif isinstance(exception, RequestException):
        return "An exception occurred while handling your request"
    elif isinstance(exception, Exception):
        return "An unexpected error occurred"
    return "An unknown openAI error occurred."
