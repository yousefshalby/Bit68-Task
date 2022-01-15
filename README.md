# Bit68-Task

<P>Hereyou can Find Bit68 task with Postgres dataBase and and tested by unittesting and Dockerized </p>

# Setup & Launch:

1. git clone https://github.com/yousefshalby/Bit68-Task.git

2. makevirtualvenv ==> python3 -m venv venv

3. source venv/bin/activate

4. cd project/

5. pip install -r requirement.txt

6. to create our Postgres database you will find credentials in (.env) file in project folder which contains settings you will find db_name and db_user and password

7. python manage.py makemigrations

8. python manage.py migrate

9. If you want to check all tests ==> python manage.py test

10. python manage.py runserver

11. DockerFile to run it all you have to do is to change DATABASE_HOST=localhost in .env to DATABASE_HOST=db

