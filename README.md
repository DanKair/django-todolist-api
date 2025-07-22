# To Do List API
## Simple API that:

✅ Allows you to sign-up, login and sign-out using JWT access / refresh tokens \
✅ Provides CRUD Operations over Tasks using task ID\
✅ Provides an admin-interface to handle User, Task models \

### To install required dependenciese, use this command: 

```pip install -r requirements.txt```

## Installation & Get Started
### 1. Cloning the Repository
```
https://github.com/DanKair/NIC-quick-tasks.git
```
### 2. Installation of dependencies
```
pip install -r requirements.txt
```

### 3. Environment Variable Configuration ( Copies the .env.sample content into .env)
```
cp .env-sample .env
```
### 4. Apply the migrations
**For Windows / MacOS users:**
```
python manage.py migrate
```
**For Linux users:**
```
python3 manage.py migrate
```
### 5. Run the server
```
python manage.py runserver
```
