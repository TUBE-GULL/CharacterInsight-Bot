<h1 align="center">Quiz for Telegram bot in Python(Aiogram)</h1>

<h2 align="center">Used Libraries</h2>
<div align="center">
  <a href="https://ydb.tech/" target="_blank" rel="noreferrer" style="display: inline-block; margin: 0 10px;">
    <img src="https://storage.yandexcloud.net/ydb-www-prod-site-assets/ydb_icon.svg" alt="ydb" width="60" height="60"/>
  </a>
  <a href="https://www.sqlite.org/index.html" target="_blank" rel="noreferrer" style="display: inline-block; margin: 0 10px;">
    <img src="https://github.com/devicons/devicon/blob/master/icons/sqlite/sqlite-original-wordmark.svg" alt="sqlite" width="60" height="60"/>
  </a>
  <!-- AIOGRAM -->
  <a href="https://docs.aiogram.dev/en/latest/index.html" target="aiogram" style="display: inline-block; margin: 0 10px;">
    <img src="https://docs.aiogram.dev/en/latest/_static/logo.png" alt="aiogram" width="60" height="60"/>
  </a>
  <!-- PYTHON -->
  <a href="https://www.python.org" target="_blank" rel="noreferrer" style="display: inline-block; margin: 0 10px;">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="60" height="60"/>
  </a>
</div>


## Installation dependencies

````bash
# install package
$ pip install aiogram
$ pip install ydb
````


## Running the app

```bash
# start in linux and mac
$ python3 main.py

# start in windows 
$ python main.py
```
# bot working 
````bash
$ /start

$ /quiz
````



# Bot Command Description

## Bot Name

Bot Username: `@CharacterInsight_bot`  
Link to Bot: [@CharacterInsight_bot](https://web.telegram.org/k/#@CharacterInsight_bot)


## Features
Start Command: Welcomes users and provides options to start the quiz with a custom keyboard.

Quiz Initialization: Users can start the quiz by typing /quiz or selecting the "Start Game" option. The quiz begins with the first question.

Question Handling: The bot sends questions one by one to the user and tracks their responses.

Answer Processing: User answers are processed via callback queries. The bot checks if the user’s response is correct and updates the quiz progress accordingly.
