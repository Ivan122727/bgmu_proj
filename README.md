# Мое Исследование Backend

[![N|Solid](https://i.imgur.com/KB4lvGM.png)](http://188.120.255.185/)

<hr>

# Ссылка на GitHub Frontend 
<h3>https://github.com/PirateThunder/med_front </h3>

<hr>

# Ссылки на решения
### Сайт с продуктом - http://188.120.255.185/
### Документация API Swagger - http://188.120.255.185/docs
### Документация API Redoc - http://188.120.255.185/redoc 

<hr>

# Реализованная функциональность на Backend
<ul>
    <li>Аунтификация пользователей</li>
    <li>Возможность менять роли пользователей</li>
    <li>Возможность редактировать пациетов</li>
    <li>Возможность редактировать исследования</li>

</ul>

<hr>

# Основной стек технологий на Backend
<ul>
    <li>Git, GitHub</li>
    <li>MongoDB 7</li>
    <li>Nginx</li>
    <li>Systemd</li>
    <li>Python 3.11</li>
    <li>FastAPI</li>
    <li>Motor</li>
    <li>Pymongo</li>
    <li>Pydantic</li>
    <li>Uvicorn</li>
    <li>Gunicorn</li>
    <li>Systemd</li>
    <li>Requests</li>
    <li>Bearer Token</li>
 </ul>

<hr>

# Deploy

### Установка Nginx
~~~
sudo apt install nginx
~~~

### Установка Python
~~~
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11
sudo apt install python3.11-venv
~~~

### Установка MongoDB 7
~~~
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl daemon-reload
sudo systemctl enable mongod
sudo systemctl restart mongod
~~~

### Создание пользователей в MongoDB
~~~
mongosh
use admin
db.createUser({
  user: "admin",
  pwd: passwordPrompt(),
  roles:[{role: "userAdminAnyDatabase" , db:"admin"}]
})
db.createUser(
{
  user: "root",
  pwd: passwordPrompt(),
  roles: ["root"]
})
db.createUser(
{
  user: "...",
  pwd: passwordPrompt(),
  roles: [
  {role: "readWrite", db: "my_research_prod"}
  ]
})
~~~

### Открытие для мира базы данных
~~~
sudo nano /etc/mongod.conf
    
net:
    port: ...
    bindIp: 127.0.0.1,...
security:
    authorization: enabled
~~~

### Создаём системного пользователя
~~~
adduser my_research
usermod -aG sudo my_research
su - my_research
~~~

### Установка poetry
~~~
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="/home/my_research/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="/home/my_research/.local/bin:$PATH"' >> ~/.profile
poetry config virtualenvs.in-project true
exec "$SHELL"
poetry --version
~~~

### Установка репозитория с GitHub
~~~
git clone git@github.com:Ivan122727/bgmu_proj.git
cd bgmu_proj
poetry env use 3.11
poetry install
~~~

### Нужно создать файл .env в папке ryadom_back и поместить туда
~~~
MONGO_HOST=...

MONGO_PORT=...

MONGO_DB_NAME=...

MONGO_USER=...

MONGO_PASSWORD=...

MONGO_AUTH_DB=...

MAILRU_LOGIN=...

MAILRU_PASSWORD=...

MAILRU_SERVER="smtp.mail.ru"

MAILRU_PORT=465
~~~

### Запуск
~~~
sudo system daemon reload
sudo systemctl start mongod
sudo systemctl start api
sudo systemctl start nginx
~~~

<hr>

# Разработчики
<h3>Илья Хакимов (https://t.me/ilyakhakimov03) - Frontend </h3>
<h3>Ермолов Иван (https://t.me/Ivan122727) - Backend, Architect </h3>
<h3>Ковтуненко Алексей Сергеевич - PM </h3>
<hr>
