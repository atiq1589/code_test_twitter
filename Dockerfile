FROM python:3.9

WORKDIR /var/www/source_code

COPY . /var/www/source_code

RUN pip install pipenv && \
    pipenv install 

CMD pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

EXPOSE 8000