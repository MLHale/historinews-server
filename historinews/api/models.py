from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
import subprocess

def validate_is_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Is not a PDF!')

class newspaper(models.Model):
    """
    This is a newspaper article
    """
    # separated by commas
    keywords = models.CharField(max_length=1000, blank=True, unique=False)
    
    newspaperName = models.CharField(max_length=1000, blank=True, unique=False)
    newspaperYear = models.IntegerField(blank=False, unique=False)
    newspaperTitle = models.CharField(max_length=1000, blank=False, unique=False)
    authorName = models.CharField(max_length=1000, blank=True, unique=False)
    newspaperCreationDate = models.DateField()
    ocrText = models.TextField(blank=False, unique=False)
    pdf = models.FileField(validators=[validate_is_pdf])
    thumb = models.ImageField()
    
    def pdfLocation(self):
        return self.pdf.url
    
    class Meta:
        verbose_name_plural = "articles"
