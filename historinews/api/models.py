from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
import subprocess

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
    thumb = models.ImageField()
    
    def pdfLocation(self):
        return self.pdf.url
    
    class Meta:
        verbose_name_plural = "articles"

# From http://www.yaconiello.com/blog/auto-generating-pdf-covers/
# What to do after a PDF is saved
def pdf_post_save(sender, instance=False, **kwargs):
    """This post save function creates a thumbnail for the PDF"""
    pdf = article.objects.get(pk=instance.pk)
    command = "convert -thumbnail 200 -extent 200x200 %s%s[0] %s%s.png" % (settings.MEDIA_ROOT, pdf.url, settings.MEDIA_ROOT, pdf.newspaperName+'_'+pdf.newspaperYear+'_'+pdf.articleTitle)

    proc = subprocess.Popen(command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout_value = proc.communicate()[0]

# Hook up the signal
post_save.connect(pdf_post_save, sender=article)