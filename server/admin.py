from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register((Category, Book, Contract, Contract_updater, Rating, Comment))


