% prepara el repositorio para su despliegue. 
release: sh -c 'cd decide && cp local_settings.heroku.py local_settings.py && cp decide/settings.heroku.py decide/settings.py && cp base/mods.heroku.py base/mods.py && python manage.py migrate'
% especifica el comando para lanzar Decide
web: sh -c 'cd decide && gunicorn decide.wsgi --log-file -'