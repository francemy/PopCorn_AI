#!/bin/sh

# Executa os três comandos desejados
python manage.py seed
python manage.py genre
python manage.py update_movie_image
