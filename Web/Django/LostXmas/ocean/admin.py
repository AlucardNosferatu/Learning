from django.contrib import admin
from ocean.models import Author, Word

# Register your models here.

admin.site.register([Author, Word])
