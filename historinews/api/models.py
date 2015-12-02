from django.db import models

class article(models.Model):
    """
    This is a newspaper article
    """
    keywords = models.CharField(max_length=20, blank=False, unique=True)
    newspaperName
    newspaperYear
    articleTitle
    authorName
    articleCreationDate
    ocrText
    pdfLocation

    class Meta:
        verbose_name_plural = "Articles"
