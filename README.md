# apsp-pars
Эта программа разработана для сбора данных с веб-страниц с использованием библиотек requests и BeautifulSoup,
а также для автоматизации взаимодействия с веб-страницами с помощью библиотеки selenium.

# Установка зависимостей
Для работы программы необходимо установить следующие зависимости:

- openpyxl - для работы с файлами Excel
- pandas - для работы с данными в формате таблицы
- selenium - для автоматизации взаимодействия с веб-страницами
- beautifulsoup4 - для парсинга HTML-кода страницы
- requests - для отправки HTTP-запросов
- psycopg2 - для работы с базой данных PostgreSQL
Вы можете установить все зависимости - из файла requirements.txt

# Подготовка к запуску
-Загрузите драйвер Chrome для Selenium и укажите путь к исполняемому файлу в переменной executable_path.
-Укажите список идентификаторов (id_names) для родительских категорий, которые нужно собрать.
-Установите необходимые заголовки (headers) для отправки запросов.

# Сбор данных
- Программа отправляет запрос на стартовую страницу и собирает ссылки на родительские категории.
- Затем происходит итерация по ссылкам родительских категорий, чтобы получить первый уровень дочерних категорий.
- Далее программа продолжает итерацию по дочерним категориям и записывает ссылки на страницы продуктов.
- После сбора всех ссылок на страницы продуктов, происходит автоматизация взаимодействия с каждой страницей продукта с помощью Selenium.
- Данные со страниц продуктов сохраняются в файл Excel (products123test.xlsx), а также в базу данных PostgreSQL.
# Использование
- Запустите программу.
- Дождитесь завершения сбора данных.
- После завершения сбора данных, программа сохранит результаты в файл Excel и загрузит их в базу данных PostgreSQL.
Примечание: Перед использованием программы, убедитесь, что у вас установлен и сконфигурирован драйвер Chrome для Selenium, а также настроена база данных PostgreSQL с соответствующими доступами.

Важно: При использовании данной программы не забудьте соблюдать правила использования данных и уважать авторские права.
