# MentAI

This project leverages Generative AI to improve mental health.
More specifically it allows users to have access to ChatGPT bot hosted on Telegram which is designed to help users exploring their psyche with questions and recommendations during virtual therapy sessions.
This bot does not in any case replace the work of a professional therapist but can hopefully help democratize the access to mental health care.

## How does it work?

The bot is built with the telegram python API and its answers are generated with ChatGPT using the OpenAI API.
Currently the model used is GPT 3.5 but alternative versions can be used by modifying the config file.
In practice several commands are available to personalize the experience (change the bot's or the user's names), start/resume/end sessions and delete the conversation's history.

## Get started

To use the bot you will have to:

- create a bot instance on Telegram (https://core.telegram.org/bots/features#botfather) and store the token in a file (for example _\_\_telegram_token.txt_ in the artifacts/ folder)
- create an OpenAI API key (https://platform.openai.com/api-keys, you will need to create an account if you do not have one already) and store it in a file (for example _\_\_openai_api_key.txt_ in the artifacts/ folder)
- run the following command lines to start the app:

```
conda create -n mentai python=3.8 -y
conda activate mentai
pip install -r requirements.txt
python app.py
```

- go to your bot conversation on Telegram and send "/start" :)

## Troubleshooting

...

## Next steps

- automatic messages from the bot for programmed sessions (e.g. once a week)
- testing other LLMs
