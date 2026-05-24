FROM python:3.12.3

WORKDIR /yandex-project

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH /yandex-project/src

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./
COPY requirements.txt ./
COPY ./images ./images
RUN pip install -r ./requirements.txt
RUN chmod +x ./src/start.sh

EXPOSE 8000

CMD ["./src/start.sh"]
