class Word(object):
    def __init__(self, rect, text):
        self.rect = rect
        self.text = text


class PageObjects(object):
    def __init__(self, page_image, words):
        self.page_image = page_image
        self.words = words