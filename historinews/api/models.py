from django.core.exceptions import ValidationError
from django.db import models

def validate_is_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Is not a PDF!')

class article(models.Model):
    """
    This is a newspaper article
    """
    keywords = models.CharField(max_length=1000, blank=True, unique=False)
    newspaperName = models.CharField(max_length=1000, blank=True, unique=False)
    newspaperYear = models.IntegerField(blank=False, unique=False)
    articleTitle = models.CharField(max_length=1000, blank=False, unique=False)
    authorName = models.CharField(max_length=1000, blank=True, unique=False)
    articleCreationDate = models.DateField()
    ocrText = models.TextField(blank=False, unique=False)
    pdf = models.FileField(validators=[validate_is_pdf])
    
    def pdfLocation(self):
        return self.pdf.url
    
    class Meta:
        verbose_name_plural = "articles"
