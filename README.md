# Foodgram
О проекте:
1. Проект Foodram собирает рецепты пользователей и позволяет исследовать новые кулинарные шедевры.
2. Написан бекенд REST API по ReDoc документации.
3. Над проектом работали:
<a href="https://github.com/Knstxx" target="_blank">Konstantin Khotnog</a>

Проект реализован в качестве дипломной работы Я.Практикума.

Tech.Stack: Python, Django, DRF, PostgreSQL, Djoser.
Сайт доступен по адрессу: https://foooooooooooodgram.sytes.net/

# Комментарии для ревью:
1. Не могу зайти в админку с сайта(!), пишет "403 CSRF verification failed. Request aborted." Попытался настроить через сеттиги - не получилось. Админка при локальном запуске с SQLite работает.
2. -
3. Поле поиска ингридиентов работает через фильры в запросах api, но не работает через графику фронта. При вводе названия ингредиента, не предлагает варианты из БД. 
4. Написал джанго-команду для загрузки в БД данных из csv файла. Настроил логику на скип существующих ингредиентов. Повторно в SQLite БД c локальной машины записи не добавляются. Однако при обновлении через CI/CD команда из воркфлоу выполняет поторное добавление строк в постгрис БД в контейнере. Не понимаю почему записывает, в моделях стоит юник, блок проверки try в команде присутствует.

---------вопросы после 1-го ревью----------

5. Я удалил сочетания в моделях типа "Blank=False, Null = False" и всё работает, но я не понимаю почему? Где я описываю обязательные поля для заполнения?

P.S. редми перепишу офк =) 
