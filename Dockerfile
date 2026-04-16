# Образ, где уже ЕСТЬ Chrome, Selenium и Python
FROM public.ecr.aws/docker/library/python:3.12-slim

# Установка Java (нужна для Allure) и curl
RUN apt-get update && apt-get install -y default-jre curl && apt-get clean

# Установка Allure (правильная ссылка на релиз)
RUN curl -o allure.tgz -L https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.tgz \
    && tar -zxvf allure.tgz -C /opt/ \
    && ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure \
    && rm allure.tgz

WORKDIR /usr/workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest"]