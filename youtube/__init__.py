from flask import Flask

app = Flask(__name__)

app.secret_key = "Ase1!tunytre543wervunws3"

from youtube import views