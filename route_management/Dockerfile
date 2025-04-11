FROM python:3.11
COPY ./src /app
WORKDIR /app
RUN pip3 install poetry && poetry install
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1337", "--reload", "--proxy-headers", "--forwarded-allow-ips=*"]
EXPOSE 1337