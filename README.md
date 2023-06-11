# Service_to_upload_save_and_download_audio_files_FastAPI
Сервис для загрузки, конвертации из 'wav' в 'mp3', хранения и предоставления возможности скачать аудио файлы. 
Приложение написано на FastAPI, в качестве БД используется PostgreSQL, при разработке применялись SQLAlchemy, Docker,
Docker-compose.
## Сборка и запуск
Для локального запуска приложения необходимо наличие установленного docker и docker-compose 
(для Linux: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04-ru).    
Затем необходимо клонировать репозиторий (в терминале: git clone 
'git@github.com:Evstud/Service_to_upload_save_and_download_audio_files_FastAPI.git').   
Далее нужно перейти в директорию с файлами приложения, там найти файл 'docker-compose.yml', 
который нужно запустить в терминале с помощью команды 'docker-compose up -d'.    
После этого произойдет создание образов и запуск контейнеров с приложением и БД.    
Проверить запущено ли приложение можно с помощью терминала и команд 'docker ps' и т.д.
Или с помощью интерфейса Swagger на который можно зайти введя в адресной строке браузера
'http://127.0.0.1:8001/docs#/'.    
Для отправки запросов в приложение можно использовать:   

1. Файл 'test_sender.py', находящийся в директории с файлами приложения. В нем - 3 функции:     
1.1 'send_user_name' - функция для создания пользователя (в аргументах функции необходимо указать имя пользователя), 
в ответ возвращаются user_id и user_token необходимые для сохранения аудио файла.     
1.2 'send_audio_file' - функция для конвертации и сохранения аудио файла (в аргументах указываются user_id, user_token 
и filepath (путь к аудиофайлу для загрузки)), возвращает ссылку для скачивания файла.     
1.3 'get_mp3' - функция для скачивания аудио файла (в аргументах необходимо указать ссылку для скачивания файла,
полученную от 'send_audio_file'. Предварительно, на 33й строчке можно изменить путь для сохранения файла
(по умолчанию mp3-файлы сохраняются в директории 'new_mp3_files' в корневой директории сервиса.
2. Http запросы на 'http://127.0.0.1'.    
2.1 Создание user. Необходимо ввести значение поля "user_name".    
```
curl -X 'POST' \
  'http://127.0.0.1:8001/create_user/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_name": "first_test"
}'
```    

Ответ:

```
{
  "user_id": "a9c9460b-2f27-49f7-a511-ac23edac2664",
  "user_token": "d0913eee-0c56-4742-abb7-f2505f6a8eea",
  "user_name": "first_test"
}
```    

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.2 Загрузка и конвертация wav-файла (файл в корневой директории). Необходимо ввести uuid пользователя и uuid token
в url, а также путь к файлку в 'file='.     

```
curl -X 'POST' \
  'http://127.0.0.1:8001/create_audio/user_id/a9c9460b-2f27-49f7-a511-ac23edac2664/user_token/d0913eee-0c56-4742-abb7-f2505f6a8eea/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@sample-15s2.wav;type=audio/wav'
```
Ответ:

```http://127.0.0.1:8001/record?id=9c07cfda-98b0-4ddd-9558-bd89a028ab2b&user=a9c9460b-2f27-49f7-a511-ac23edac2664```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.3 Скачивание файла из БД. Необходимо ввести ссылку полученную в ответ на запрос 2).    

```
curl -X 'GET' \
  'http://127.0.0.1:8001/record?id=9c07cfda-98b0-4ddd-9558-bd89a028ab2b&user=a9c9460b-2f27-49f7-a511-ac23edac2664' \
  -H 'accept: application/json'
```
В ответ вернется словарь с ключами: 'audio_name' - имя файла, 'audio_data' - сериализованная base64-строка. 
Для получения mp3 файла необходимо десериализовать данную строку в файл (на python с помощью модуля 'base64').

3. Интерфейс Swagger. Методы:     
3.1 'Create User' (ввести имя пользователя). В ответ вернется словарь с 'user_id', 'user_token', 'user_name'.    
3.2 'Save Audio' (ввести user_id и user_token, выбрать файл). В ответ вернется ссылка для скачивания mp3-файла.    
3.3 'Get Audio' (ввести id (audio_id) и user (user_id)).    
В ответ вернется словарь с ключами: 'audio_name' - имя файла, 'audio_data' - сериализованная base64-строка. 
Для получения mp3 файла необходимо десериализовать данную строку в файл (на python с помощью модуля 'base64').


