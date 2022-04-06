import fitz
import PIL

from tables_extractor.page_objects import Word, PageObjects
from tables_extractor.rect import Rect


class PageObjectsCreator(object):
    def create_from_path(self, pdf_file_path):
        """Returns list of PageObjects. Length of list is equal to pages count."""
        
        doc = fitz.open(pdf_file_path)
        return self._do_create(doc)

    def create_from_bytes(self, pdf_file_data):
        doc = fitz.open(stream=pdf_file_data, filetype='pdf')
        return self._do_create(doc)

    def _do_create(self, document):
        result = []
        for page in document:
            result.append(
                PageObjects(self._get_page_image(page), self._get_words(page))
            )

        return result

    def _get_page_image(self, page):
        pixmap = page.get_pixmap(dpi=72)
        size = (pixmap.width, pixmap.height)
        return PIL.Image.frombuffer('RGB', size, pixmap.samples)

    def _get_words(self, page):
        text_page = page.get_textpage()
        words = text_page.extractWORDS()

        result = []
        for word in words:
            left, top, right, bottom, text, *_ = word
            result.append(Word(Rect(left, top, right, bottom), text))

        return result

