# MentAI chatbot
import datetime as dt
import json

from openai import OpenAI
from telegram import Update
from telegram.ext import ContextTypes

from .config import *
from .prompt import *

API_KEY = open(f"{ROOT_PATH}/{API_KEY_PATH}", 'r').read()
DEFAULT_CONFIG = {
    "bot_name": DEFAULT_BOT_NAME,
    "user_name": "",
    "history": [{"role": "system", "content": CONTEXT_PROMPT}],
    "llm_params": LLM_PARAMS,
    "save_path": HISTORY_PATH,
}
client = OpenAI(api_key=API_KEY)


class Mentai:
    """Psychologist Telegram chatbot class based on openai's ChatGPT API.
    """

    def __init__(self, client: OpenAI = client, config: dict = DEFAULT_CONFIG) -> None:
        """
        :param client: OpenAI, defaults to client.
            OpenAI API client.
        :param config: dict, defaults to DEFAULT_CONFIG.
            configuration dictionary for the bot.
        """
        self.client = client
        self.bot_name = config.get('bot_name', DEFAULT_CONFIG['bot_name'])
        self.user_name = config.get('user_name', DEFAULT_CONFIG['user_name'])
        self.history = config.get('history', DEFAULT_CONFIG['history'])
        self.llm_params = config.get('llm_params', DEFAULT_CONFIG['llm_params'])
        self.save_path = config.get('save_path', DEFAULT_CONFIG['save_path'])

    @staticmethod
    def display_dict(dict: dict):
        output = ""
        for k, v in dict.items():
            output = output + f" - {k}: {v}\n"
        return output
    
    @staticmethod
    def postprocess(text):
        text_ = text.replace("Psychologist: ", "")
        return text_

    def generate_response(self, messages:list):
        completion = self.client.chat.completions.create(messages=messages, **self.llm_params)
        output = self.postprocess(completion.choices[0].message.content)

        return output
    
    def save(self):
        """Saves the configuration and messages to the sepcified location
        """
        with open(f"{ROOT_PATH}/{self.save_path}/mentai_{dt.datetime.now().strftime(format='%Y-%m-%d_%H%M')}.json", "w") as file:
            json.dump({
                "bot_name": self.bot_name,
                "user_name": self.user_name,
                "history": self.history,
                "llm_params": self.llm_params,
            }, file)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = START_PROMPT):
        """Bot initialization message.
        """
        text_ = (
            text
            .replace("{bot_name}", self.bot_name)
            .replace("{command_dict}", self.display_dict(COMMAND_DICT))
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text_)

    async def username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = USERNAME_PROMPT):
        """Updates the user name
        """
        self.user_name = " ".join(context.args)
        text_ = text.replace("{user_name}", self.user_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text_)

    async def botname(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = BOTNAME_PROMPT):
        """Updates the bot name
        """
        self.bot_name = " ".join(context.args)
        text_ = text.replace("{bot_name}", self.bot_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text_)
    
    async def delete(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = DELETE_PROMPT):
        """Deletes the history
        """
        self.history = self.history[:1]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    
    async def end(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ends the session
        """
        self.history.append({"role": "user", "content": "I would like to end the session for today."})
        response = self.generate_response(self.history)
        self.history.append({"role": "assistant", "content": response})
        self.save()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    async def reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Replies to the message sent by the user
        """
        self.history.append({"role": "user", "content": update.message.text})
        response = self.generate_response(self.history)
        self.history.append({"role": "assistant", "content": response})
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    async def new(self, update: Update, context: ContextTypes.DEFAULT_TYPE, prompt: str = NEW_PROMPT):
        """Starts a new session
        """
        self.history.append({"role": "system", "content": prompt.replace("{user_name}", self.user_name)})
        response = self.generate_response(self.history)
        self.history.append({"role": "assistant", "content": response})
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    async def resume(self, update: Update, context: ContextTypes.DEFAULT_TYPE, prompt: str = RESUME_PROMPT):
        """Resumes the previous session
        """
        self.history.append({"role": "system", "content": prompt.replace("{user_name}", self.user_name)})
        response = self.generate_response(self.history)
        self.history.append({"role": "assistant", "content": response})
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
