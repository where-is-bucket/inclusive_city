FROM python:3.11

COPY ./app /web-api/app
COPY start.sh /web-api/start.sh

WORKDIR /web-api
RUN pip install -r ./app/requirements.txt

ENTRYPOINT ["./start.sh"]
EXPOSE 8000