"""

"""
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

def read_in(fname):
    fp = file(fname, 'rb')
    laparams = LAParams()
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, sys.stdout, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()
    device.close()