from django.contrib import admin
from django import forms
from historinews.api.models import newspaper
from historinews.widgets import admin_article_thumnail_widget


class newspaper_admin(admin.ModelAdmin):
    list_display = ('newspaperName', 'newspaperYear', 'newspaperTitle')

admin.site.register(newspaper, newspaper_admin)
