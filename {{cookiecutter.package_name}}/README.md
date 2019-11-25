# migration
create a migration repository 
`
flask db init
`

generate an initial migration
``
flask db migrate
``

apply the migration to the database
`
flask db upgrade
`

env FLASK_APP=run.py flask run

# script 

`
python manager.py runserver | db 
`

# template
`cookiecutter /Users/chen/myPoject/friends/friends_backend/py_cookiecutter/my_template
`
