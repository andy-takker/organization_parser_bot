FROM python:3.11-slim
RUN pip install -U --no-cache-dir poetry pip && poetry config virtualenvs.create false

WORKDIR /bot

COPY ./pyproject.toml ./poetry.lock /bot/
RUN poetry install --no-interaction --no-ansi --no-root --without dev

ENV PYTHONPATH=/bot/

COPY ./src/ /bot/src

RUN chmod +x ./src/start.sh                                                      

ENTRYPOINT [ "/bot/src/start.sh" ]