FROM python:3.13-slim
RUN apt update && apt install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main
COPY quizbot ./quizbot
CMD [ "poetry", "run", "python", "quizbot/run.py" ]
