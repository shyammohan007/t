from django.contrib import admin

from bank_app.models import *

MODEL_LIST = [
    Account, Transaction
]

for model in MODEL_LIST:
    admin.site.register(model)