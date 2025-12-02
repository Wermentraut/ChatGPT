# ChatGPT repo: краткое использование скриптов

Все команды выполнять из `C:\Users\artem\Documents\GitHub\ChatGPT`.

## calculator.py
Простой калькулятор с вводом одной операции.
- Запуск: `python calculator.py`
- Вводите через пробел: `<a> <op> <b>` (пример: `2 + 3`, `10 / 4`, `2 ** 5`).

## inverse_finder.py
Символьный поиск обратной функции с помощью SymPy.
- Базовый пример:  
  `python inverse_finder.py "x**2 + 3" --input-var x --output-var y`
- Если выражение не передано, скрипт спросит его.
- Ключи: `--input-var`, `--output-var`, `--inverse-input-var`, `--domain (real|complex)`.

## zeta.py
Вычисление дзета-функции Римана для действительных и комплексных s.
- Демонстрация по умолчанию: `python zeta.py`
- Свои значения без вопросов: `python zeta.py 2 -1 0.5+14j`
- Интерактивный ввод: запустите без аргументов и введите числа через пробел (комплексные в виде `0.5+14j`).  
- Настройка точности: `--max-terms 500000 --tol 1e-14` (например: `python zeta.py 2 --max-terms 500000 --tol 1e-14`).

## discord_bot.py
Discord-бот с ChatGPT-подобными ответами через локальный Ollama (бесплатно, без внешних API).
- Установка: `pip install -U discord.py requests`
- Создайте бота и токен: https://discord.com/developers/applications
- Переменная токена:  
  PowerShell: `$env:DISCORD_BOT_TOKEN="ваш_токен"`  
  CMD: `set DISCORD_BOT_TOKEN=ваш_токен`
- Ollama: https://ollama.com/download → `ollama pull llama3` (по умолчанию ждём http://127.0.0.1:11434). Можно менять `OLLAMA_URL`, `OLLAMA_MODEL`.
- Запуск: `python discord_bot.py`
- Команды: `!ping`, `!roll [max]`, `!gpt <сообщение>` (короткая история канала сохраняется для контекста).
