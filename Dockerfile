FROM mcr.microsoft.com/azure-functions/python:3.0-python3.7-appservice

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    git

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /home/site/wwwroot