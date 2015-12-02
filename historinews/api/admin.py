from django.contrib import admin
from django import forms
from historinews.api.models import article
from historinews.widgets import admin_article_thumnail_widget

class article_admin_form(forms.ModelForm):
    class Meta:
        model = article
        fields = ('keywords', 'newspaperName', 'newspaperYear', 'articleTitle', 'authorName', 'articleCreationDate', 'ocrText', 'pdf')
        widgets = {
            'thumbnail' : admin_article_thumnail_widget(),
        }

class article_admin(admin.ModelAdmin):
    list_display = ('newspaperName','newspaperYear','articleTitle')
    form = article_admin_form

admin.site.register(article, article_admin)
