import os

ROOT_PATH = f"{os.getcwd().split('mentai')[0]}\\mentai"

DEFAULT_BOT_NAME = "Dr. Mentai"

COMMAND_DICT = {
    "/new": "to start a new session with me",
    "/resume": "to continue the previous session",
    "/end": "to terminate the session in progress",
    "/username": "to configure the name you would like me to use in our sessions. For instance, if you would like me to call you John, type '/username John'",
    "/botname": "to change my name. For instance, if you would like me to be called Dr. House, type '/botname Dr. House'",
    "/delete": "to erase the content of all our previous discussions",
}

LLM_PARAMS = {
    "model": "gpt-3.5-turbo",
    "max_tokens": 100,
    "temperature": 0.2,
}

API_KEY_PATH = "artifacts/__openai_api_key.txt"

TELEGRAM_TOKEN_PATH = "artifacts/__telegram_token.txt"

HISTORY_PATH = "artifacts/"