FROM python:3.12.3

ENV PATH="${PATH}:/root/.local/bin"
COPY src /app/src
COPY alembic /app/alembic
COPY alembic.ini /app/
COPY requirements.txt /app/
COPY ./images /images

ENV PYTHONPATH /app/src
WORKDIR /app
RUN pip install -r ./requiriments.txt
RUN chmod +x ./src/start.sh
EXPOSE 8000
