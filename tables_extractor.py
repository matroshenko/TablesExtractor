
class Cell(object):
    def __init__(self, grid_rect, recognized_text):
        self._grid_rect = grid_rect
        self._recognized_text = recognized_text


class Table(object):
    def __init__(self, grid_structure, cells):
        self._grid_structure = grid_structure
        self._cells = cells


class TablesExtractor(object):
    def __init__(self, page_objects):
        self._page_objects = page_objects

    def extract(self):
        pass