from django.db import models

class article(models.Model):
    """
    This is a newspaper article
    """
    keywords = models.CharField(blank=True, unique=False)
    newspaperName = models.CharField(blank=True, unique=False)
    newspaperYear = models.IntegerField(blank=False, unique=False)
    articleTitle = models.CharField(blank=False, unique=False)
    authorName = models.CharField(blank=True, unique=False)
    articleCreationDate = models.DateField()
    ocrText = models.TextField(blank=False, unique=True)
    pdfLocation = models.FileField()

    class Meta:
        verbose_name_plural = "Articles"
