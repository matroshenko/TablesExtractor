from tables_finder import TablesFinder
from table_analyzer import TableAnalyzer
from cell_text_recognizer import CellTextRecognizer


class Cell(object):
    def __init__(self, grid_rect, text):
        self.grid_rect = grid_rect
        self.text = text


class Table(object):
    def __init__(self, grid_structure, cells):
        self.grid_structure = grid_structure
        self.cells = cells


class TablesExtractor(object):
    def __init__(self, page_objects):
        self._page_objects = page_objects

    def extract(self):
        tables_finder = TablesFinder(self._page_objects)
        rects = tables_finder.find()

        tables = []
        for rect in rects:
            table_analyzer = TableAnalyzer(self._page_objects, rect)
            grid_structure, cells_grid_rects = table_analyzer.analyze()
            cells = []
            for cell_grid_rect in cells_grid_rects:
                cell_rect = grid_structure.get_cell_rect(cell_grid_rect)
                cell_text_recognizer = CellTextRecognizer(self._page_objects, cell_rect, True)
                text = cell_text_recognizer.recognize()
                cells.append(Cell(cell_grid_rect, text))

            tables.append(Table(grid_structure, cells))  
                      
        return tables