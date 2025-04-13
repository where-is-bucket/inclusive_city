FROM python:3.11
COPY ./app /web-api/app
WORKDIR /web-api
RUN pip install -r ./app/requirements.txt
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000", "--reload", "--proxy-headers"]
EXPOSE 8000