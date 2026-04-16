#FROM python:3.12-slim
# Берем образ, где уже ЕСТЬ Chrome, Selenium и Python
#FROM seleniarm/standalone-chromium:latest
FROM public.ecr.aws/docker/library/python:3.12-slim

## Устанавливаем ТОЛЬКО Java (для Allure) и минимум библиотек
## 1. Системные зависимости + Java + curl
#RUN apt-get update --fix-missing && apt-get install -y \
#    default-jre \
#    wget \
#    gnupg \
#    curl \
#    unzip \
#    && apt-get clean

    ## 2. Установка Chrome (правильные ссылки!)
    #RUN wget -q -O - https://google.com | apt-key add - \
    #    && echo "deb [arch=amd64] http://google.com stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    #    && apt-get update && apt-get install -y google-chrome-stable

#RUN apt-get update && apt-get install -y chromium chromium-driver
#
# Ставим Java (нужна для Allure) и curl
RUN apt-get update && apt-get install -y default-jre curl && apt-get clean
# 3. Установка Allure (правильная ссылка на релиз)
RUN curl -o allure.tgz -L https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz \
    && tar -zxvf allure.tgz -C /opt/ \
    && ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure \
    && rm allure.tgz

WORKDIR /usr/workspace

#RUN apk add --no-cache openjdk11-jre curl tar bash
#
#
#RUN curl -o allure.tgz -L https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz \
#    && mkdir -p /opt \
#    && tar -zxvf allure.tgz -C /opt/ \
#    && ln -s /opt/allure-2.24.1/bin/allure /usr/bin/allure \
#    && rm allure.tgz

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest"]