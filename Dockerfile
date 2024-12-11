FROM python:3.12.5
ENV PYTHONUNBUFFERED 1
WORKDIR /bunker
ADD ./bunker .
COPY . .
RUN pip install -r requirements.txt
