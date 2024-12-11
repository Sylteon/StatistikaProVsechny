from django.contrib import admin
from .models import Tag, Category, Article, CSVFile

admin.register(Tag)
admin.register(Category)
admin.register(Article)
admin.register(CSVFile)
