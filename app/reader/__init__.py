# -*— coding:utf-8 -*—
from flask import Blueprint

reader = Blueprint('function',__name__)

from . import forms, views, errors