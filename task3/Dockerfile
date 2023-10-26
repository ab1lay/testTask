# Установка базового образа
FROM python:3.9

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости проекта (например, requirements.txt)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Команда для запуска вашего приложения
CMD [ "python", "main.py" ]
