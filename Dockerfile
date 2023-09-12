FROM python:3.11-slim
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.create false

WORKDIR /bot

COPY ./pyproject.toml ./poetry.lock /bot/

RUN poetry export -f requirements.txt --output /bot/requirements.txt \
    --without-hashes --without-urls \
    && pip install -r /bot/requirements.txt


ENV PYTHONPATH=/bot/

COPY ./src/ /bot/src

RUN  alembic -c src/alembic.ini upgrade head                                                          

CMD [ "python", "./src/bot/cli.py" ]