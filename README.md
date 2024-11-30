# GOAT LLL Browser and Server

Это простой браузер и сервер на основе нашего собственного протокола LLL. Сервер обслуживает HTML-контент из папки, а клиент реализован на `tkinter` и `tkhtmlview`, что позволяет показывать HTML-страницы локально через созданный LLL-протокол.

## Установка

   
1. Установите зависимости:
    ```bash
    pip install tkhtmlview
    ```

## Настройка

### Сервер

1. Убедитесь, что у вас есть папка `sites` в корневом каталоге проекта.
2. Поместите HTML файлы с расширением `.lll` в папку `sites`. Имя файла будет использоваться как домен.
3. Запустите сервер:
    ```bash
    python server.py
    ```
   По умолчанию сервер будет прослушивать порт 8080. Щелкните порт до открытия для внешних подключений, отредактировав server.py для манипуляции с использованием адреса '0.0.0.0'.

### Клиент

1. Запустите клиентское приложение:
    ```bash
    python browser.py
    ```
   
2. В меню "File" выберите "Set Server IP" и введите IP-адрес сервера (например, `localhost` для локального запуска или внешний IP-адрес).

3. Введите имя файла (например, `example.lll`) в поле URL и нажмите "Load Page", чтобы загрузить HTML-содержимое с сервера.

## Заметки

- Чтобы сервер принимал подключения из интернета, убедитесь, что брандмауэр настроен правильно и порт 8080 открыт (если хотите - другой).
- Для локальной работы и тестирования используйте `localhost` в качестве IP.

## Лицензия

Этот проект лицензирован под MIT License - см. файл LICENSE для деталей.