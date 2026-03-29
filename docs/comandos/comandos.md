pip install -r install.txt
django-admin startproject 'nome_projeto'
python manage.py startapp 'nome_arquivo'

Para criar a migration (novas tabelas ou colunas)
    python manage.py makemigrations

Para subir essas atualizações:
    python manage.py migrate 

Para rodar o projeto:
    python manage.py runserver