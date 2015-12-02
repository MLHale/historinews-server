from django.contrib import admin
from historinews.api.models import *

class articleAdmin(admin.ModelAdmin):
    list_display = ('articleTitle','newspaperYear')

admin.site.register(article, articleAdmin)
