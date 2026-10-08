# Установка и запуск на macOS

## 1. Установить uv

`uv` устанавливает Python и зависимости проекта, а также запускает программу в виртуальном окружении.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

закрыть и заново открыть терминал, затем проверить установку:

```bash
uv --version
```

## 2. Скачать проект

```bash
git clone https://github.com/27xyline/alg_lab.git
cd alg_lab
```

дальнейшие команды выполнять из папки `alg_lab`

## 3. Установить Python и зависимости

```bash
uv python install 3.14
uv sync
```

- `uv python install 3.14` устанавливает нужную версию Python.
- `uv sync` создаёт виртуальное окружение `.venv` и устанавливает зависимости по файлу `uv.lock`. Вручную активировать окружение не нужно.

## 4. Запустить проект

```bash
uv run main.py
```
