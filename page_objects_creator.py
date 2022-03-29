import fitz
import PIL

from page_objects import Word, PageObjects
from rect import Rect


class PageObjectsCreator(object):
    def create(self, pdf_file_path):
        """Returns list of PageObjects. Length of list is equal to pages count."""
        
        doc = fitz.open(pdf_file_path)
        result = []
        for page in doc:
            result.append(
                PageObjects(self.get_page_image(page), self.get_words(page))
            )

        return result

    def get_page_image(self, page):
        pixmap = page.get_pixmap(dpi=72)
        size = (pixmap.width, pixmap.height)
        return PIL.Image.frombuffer('RGB', size, pixmap.samples)

    def get_words(self, page):
        text_page = page.get_textpage()
        words = text_page.extractWORDS()

        result = []
        for word in words:
            left, top, right, bottom, text, *_ = word
            result.append(Word(Rect(left, top, right, bottom), text))

        return result

