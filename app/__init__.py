from flask import Flask

app = Flask(__name__)
botlist = {}

from app import run
