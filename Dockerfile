# syntax=docker/dockerfile:1
FROM python:3.9-alpine3.15
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENV=PROD

ARG SECRET_KEY
ARG ALLOWED_HOSTS
ARG CORS_ALLOWED_ORIGINS
ARG PAULSOFT_EMAIL_USER
ARG PAULSOFT_EMAIL_PASSWORD
ARG DATABASE_URL
ARG PORT
ARG EMAIL_VERIFICATION_URL

ENV PORT=$PORT
ENV SECRET_KEY=$SECRET_KEY
ENV ALLOWED_HOSTS=$ALLOWED_HOSTS
ENV CORS_ALLOWED_ORIGINS=$CORS_ALLOWED_ORIGINS
ENV PAULSOFT_EMAIL_USER=$PAULSOFT_EMAIL_USER
ENV PAULSOFT_EMAIL_PASSWORD=$PAULSOFT_EMAIL_PASSWORD
ENV EMAIL_VERIFICATION_URL=$EMAIL_VERIFICATION_URL
ENV DATABASE_URL=$DATABASE_URL

WORKDIR /usr/src/app
COPY requirements.txt ./

#Install MSSQL driver and C++/C dependencies:

RUN apk update
RUN apk -U add gcc libc-dev g++ libffi-dev unixodbc-dev curl gnupg
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.8.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.8.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.8.1.1-1_amd64.sig
RUN curl -O https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.8.1.1-1_amd64.sig
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --import -
RUN gpg --verify msodbcsql17_17.8.1.1-1_amd64.sig msodbcsql17_17.8.1.1-1_amd64.apk
RUN gpg --verify mssql-tools_17.8.1.1-1_amd64.sig mssql-tools_17.8.1.1-1_amd64.apk
RUN apk add --allow-untrusted msodbcsql17_17.8.1.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools_17.8.1.1-1_amd64.apk

# Configure server

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE $PORT
CMD gunicorn GradesApp.wsgi:application --bind 0.0.0.0:$PORT --timeout 0

#DOCS:
#https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
#https://docs.docker.com/samples/django/
#https://wiki.alpinelinux.org/wiki/Package_management
#https://stackoverflow.com/questions/51888064/install-odbc-driver-in-alpine-linux-docker-container