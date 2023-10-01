# R4C

Тестовое задание от BST Digital.

## Описание

Данный проект - это выполнение тестового задания. [Ссылка](https://github.com/AngelinaCher/R4C/blob/master/tasks.md)
на задачи. Задание рассчитано на Django без использования DFR.

## Установка

1. Склонируйте репозиторий: `git clone https://github.com/AngelinaCher/R4C.git `
2. Перейдите в директорию проекта `cd R4C`
3. Создайте виртуальное окружение: `python -m venv venv`
4. Активируйте виртуальное окружение:
    * Для Windows: `venv\Scripts\activate`
    * Для Linux: `source venv/bin/activate`
5. Установите зависимости: `pip install -r requirements.txt`
6. Примените миграции: `python manage.py makemigrations` и `python manage.py migrate`
7. Создайте суперпользователя: `python manage.py createsuperuser`
8. Запустите сервер разработки: `python manage.py runserver`

### Установка с использованием Poetry

1. Склонируйте репозиторий: `git clone https://github.com/AngelinaCher/R4C.git `
2. Перейдите в директорию проекта `cd R4C`
3. Активируйте виртуальное окружение: `poetry shell`
4. Установите зависимости с помощью Poetry: `poetry install`
5. Примените миграции: `python manage.py makemigrations` и `python manage.py migrate`
7. Создайте суперпользователя: `python manage.py createsuperuser`
8. Запустите сервер разработки: `python manage.py runserver`

## Использование
* Task 1:
Для добавления данных в БД, нужно отправить POST-запрос на адрес: http://127.0.0.1:8000/robots/api/v1/create-robot-record/
В теле запроса - данные о заказе в формате JSON:  `{"model":"R2","version":"D2","created":"2022-12-31 23:59:59"}`

* Task 2:
Для того, чтоб получить прямую ссылку на скачивание отчёта, нужно перейти по ссылке: http://127.0.0.1:8000/orders/get-report/
Далее нажать на кнопку "Сформировать", после чего появится ссылка на скачивание excel-файла.

* Task 3:
Отправляется POST-запрос на адрес: http://127.0.0.1:8000/orders/api/v1/process-order/
В теле запроса - данные о заказе в формате JSON: `{"customer_id": 4, "robot_serial": "R2-D2", "order_date": "2023-09-30"}`
Если робот есть в наличии, то отправляется письмо на email, если его нет, то статус заказа изменится на "Ожидание".
После появления робота в наличии, клиенту отправятся email.

## Технологии
* Python 3.10.12
* Django 4.2.5
* JavaScript
* openpyxl 3.1.2

## Структура проекта
* [customers](customers) - приложение клиенты
* [media](media) - директория для хранения сформированных отчётов
  + [report-24.09.2023-01.10.2023.xlsx](media%2Freport-24.09.2023-01.10.2023.xlsx) - пример отчёта
* [orders](orders) - приложение заказы
   + [services](orders%2Fservices) - бизнес-логика по работе с заказами
      + [create_link_to_report.py](orders%2Fservices%2Fcreate_link_to_report.py) - получение прямой ссылки для скачивания
      + [create_order.py](orders%2Fservices%2Fcreate_order.py) - обработка заказа
   + [signals](orders%2Fsignals) - сигналы
      + [signals.py](orders%2Fsignals%2Fsignals.py) - проверка заказов со статусом "Ожидание" и уведомление клиентов, при добавлении робота
* [R4C](R4C) - проект R4C
* [robots](robots) - приложение роботы
    + [services](robots%2Fservices) - бизнес-логика по работе с роботами
        + [add_robot.py](robots%2Fservices%2Fadd_robot.py) - добавление робота
* [utils](utils) - утилиты
   + [excel_generator.py](utils%2Fexcel_generator.py) - формирование excel-файла
   + [send_notification.py](utils%2Fsend_notification.py) - отправка уведомления на email
* [.gitignore](.gitignore) - gitignore-файл
* [db.sqlite3](db.sqlite3) - база данных
* [manage.py](manage.py) - управления Django проектом
* [task_README.md](task_README.md) и [tasks.md](tasks.md) - задание
