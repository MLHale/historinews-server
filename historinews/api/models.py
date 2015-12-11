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
    _keywords = models.CharField("Keywords", max_length=1000, blank=True, unique=False, help_text="Keywords should be separated by commas  <br/>&nbsp;&nbsp; Example) 'the boy, the girl, 3rd keyword'")
    
    newspaperName = models.CharField(max_length=1000, blank=True, unique=False)
    newspaperYear = models.IntegerField(default=0, unique=False)
    newspaperTitle = models.CharField(max_length=1000, blank=False, unique=False)
    authorName = models.CharField(max_length=1000, blank=True, unique=False)
    newspaperCreationDate = models.DateField(help_text="Input as YYYY-MM-DD  <br/>&nbsp;&nbsp; Example) '1995-02-15'")
    ocrText = models.TextField(default="", blank=True, unique=False, help_text="<b>Either enter the OCR text of the PDF yourself or let the uploader pull it out.<br/>NOTE: this will take a while, depending on the size of the PDF.<b>")
    pdf = models.FileField(validators=[validate_is_pdf])
    #thumb = models.ImageField()
    thumb_name = models.CharField(default='', max_length=200, blank=True, unique=False)
    
    def pdfLocation(self):
        return self.pdf.url
    
    def thumb(self):
        return '{dirpath}/{filename}'.format(dirpath=settings.SUB_MEDIA_URL, filename=self.thumb_name)

    def keywords(self):
      keywords = self._keywords.split(',')
      for i in range(len(keywords)):
          keywords[i] = keywords[i].strip()
      return keywords

    class Meta:
        verbose_name_plural = 'newspapers'
