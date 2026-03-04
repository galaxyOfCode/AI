"""
This module contains functions for handling various types of errors. 
"""

import openai
from requests.exceptions import HTTPError, Timeout, RequestException


def handle_file_errors(exception: Exception) -> str:
    """Handles file-related errors and returns user-friendly messages."""

    if isinstance(exception, FileNotFoundError):
        return "Error: The file was not found."
    if isinstance(exception, PermissionError):
        return "Error: Permission denied when trying to read the file."
    if isinstance(exception, OSError):
        return "Error: An error occurred while reading from the file."
    return "An unknown file error occurred."


def handle_openai_errors(exception: openai.OpenAIError) -> str:
    """Handles OpenAI API errors and returns user-friendly messages."""

    if isinstance(exception, openai.APIConnectionError):
        return "The server could not be reached\n" + \
            str(exception.__cause__)
    if isinstance(exception, openai.RateLimitError):
        return "A 'Rate Limit Notice' was received; we should back off a bit."
    if isinstance(exception, openai.APIStatusError):
        return "A non-200-range status code was received: " + \
            str(exception.status_code) + " " + str(exception.response)
    return "An unknown openAI error occurred."


def handle_request_errors(exception: RequestException) -> str:
    """Handles general request errors and returns user-friendly messages."""
    if isinstance(exception, HTTPError):
        return "An HTTP error occurred"
    if isinstance(exception, Timeout):
        return "The request timed-out"
    if isinstance(exception, RequestException):
        return "An exception occurred while handling your request"
    if isinstance(exception, Exception):
        return "An unexpected error occurred"
    return "An unknown openAI error occurred."
