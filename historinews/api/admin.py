from django.contrib import admin
from django import forms
from django.conf import settings
from historinews.api.models import newspaper
from historinews.widgets import admin_article_thumnail_widget
from wand.image import Image
import os
from historinews.pdf import read_in
from subprocess import Popen, PIPE
from threading import Thread


ADMIN_DESCRIPTION = """
<div class="form-row">
  <h1>Note:</h1>
  <h3>
    <b>Bold</b> fields are required
  </h3>
  <br/><br/><br/>
</div>
"""

def gen_ocr(obj):
    proc = Popen(['pdf2txt.py', obj.pdf.path], stdout=PIPE)
    out = proc.communicate()[0]
    obj.ocrText = out
    obj.save()

class newspaper_admin(admin.ModelAdmin):
    list_display = ('id', 'newspaperTitle', 'newspaperCreationDate')
    fieldsets = (
        (None, {
            'fields': ('_keywords', 'newspaperName', 'newspaperTitle', 'authorName', 'newspaperCreationDate', 'pdf', 'ocrText'),
            'description': ADMIN_DESCRIPTION,
        }),
    )

    def get_form(self, request, obj, **kwargs):
        self.exclude = ('thumb_name', 'newspaperYear')
        return super(newspaper_admin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        resp = super(newspaper_admin, self).save_model(request, obj, form, change)
        
        # Create year field
        obj.newspaperYear = obj.newspaperCreationDate.year
        
        # Create thumbnail
        _thumbnail_name = '{name}.{ext}'.format(name=obj.id, ext='jpg')
        _thumbnail_path = os.path.join(settings.SUB_MEDIA_ROOT, _thumbnail_name)
        with Image(filename='{path}[{page}]'.format(path=obj.pdf.path, page=0)) as img:
          #img.resize(200, 150)
          img.resize(385, 500)
          img.save(filename=_thumbnail_path)
        obj.thumb_name = _thumbnail_name

        # Grab OCRed text from PDF
        if not obj.ocrText:
            obj.ocrText = "Loading OCR text. Please wait..."
            proc = Thread(target=gen_ocr, args=(obj,))
            proc.start()
        
        # Save object again
        obj.save()
        return resp

admin.site.register(newspaper, newspaper_admin)
