# Emergency Notification Service(Система оповещения ЧП)

## Defeniton

Этот сервис был написан потому что, я хотел создать полезный продукт,
который при этом будет работать под большими нагрузками.

Пользователь может добавить несколько других людей со всеми их контактными данными.
Затем создать шаблон сообщения которое по нажатию кнопоки будет отправленно всем его
получателям которых он выюрал заранее на те девайсы которые они указали как свои контакты 


## Запуск проекта


 docker compose up --build 
 открыть новый терминал и в нем написать 
 docker exec -it notify_app bash 
 
 cd .. 
 alembic upgrade head 
 psql -U postgres
 


## Как пользоваться
    Загрузка пользователей с контактами через ,csv файл, содержащий 3 колонки

    Имя Телефон Электронную почту

    Создание шаблонов нотификаций и конфигураций нужных получателей 
    
    Отправка нотификаций на любой девайс получателя автоматически при 
    отправке нотификаций всей группе получателей


## Авторы 
ALLGareLL115