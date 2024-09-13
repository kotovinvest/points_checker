# Код для получения данных о количестве поинтов в проектах: Fuel, Karak, EtherFi, Usual, Reya
## *Функционал:*
Чтение списка кошельков из файла wallets.txt.

Чтение списка прокси из файла proxy.txt.

Выполнение HTTP-запросов к API для получения данных о поинтах

Сохранение результатов в Excel-файл.

Обработка ошибок запросов и подключений.


## *Используемые библиотеки:*
requests — для отправки HTTP-запросов.

pandas — для обработки и сохранения данных в Excel.

itertools.cycle — для циклического использования прокси.

## *Результаты:*
После завершения работы, данные сохранятся в Excel-файле:

Для каждого отдельного протокола — в файле вида karak_wallets_data.xlsx.

При выборе всех протоколов одновременно — в файле all_protocols_stat.xlsx, где каждому протоколу будет выделен отдельный лист.

