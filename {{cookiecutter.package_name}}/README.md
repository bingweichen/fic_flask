# Running locally
1. install requirements
```
pip install -r requirements
```

2. migrate database
```
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
```
3. run server

```
python manager.py runserver
```


# migration
create a migration repository 
`
python manager.py db init
`
generate an initial migration
``
python manager.py db migrate
``

apply the migration to the database
`
python manager.py db upgrade
`
# script 
`
python manager.py runserver | db 
`

# create app (template)
`
cookiecutter https://github.com/bingweichen/fic_flask_create_app.git
`
