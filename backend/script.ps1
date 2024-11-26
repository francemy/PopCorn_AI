Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.\.venv\Scripts\activate
pip install -r requirements.txt

pip install python-dotenv

$env:FLASK_APP="wsgi.py"
$env:FLASK_ENV="development"
flask run


