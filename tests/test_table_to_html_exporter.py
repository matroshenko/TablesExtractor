from unittest import TestCase, main
import xml.etree.ElementTree as ET

import context
from tables_extractor.rect import Rect
from tables_extractor.tables_extractor import Cell
from tables_extractor.table_to_html_exporter import TableToHTMLExporter


class TablesExtractorTestCase(TestCase):
    def test_simple(self):
        cells = [
            Cell(Rect(0, 0, 1, 2), '0'),
            Cell(Rect(1, 0, 2, 1), '1'),
            Cell(Rect(2, 0, 3, 1), '2'),
            Cell(Rect(3, 0, 4, 1), '3'),
            Cell(Rect(1, 1, 3, 2), '4'),
            Cell(Rect(3, 1, 4, 2), '5'),
            Cell(Rect(0, 2, 1, 3), '6'),
            Cell(Rect(1, 2, 2, 4), '7'),
            Cell(Rect(2, 2, 3, 3), '8'),
            Cell(Rect(3, 2, 4, 3), '9'),
            Cell(Rect(0, 3, 1, 4), '10'),
            Cell(Rect(2, 3, 4, 4), '11')
        ]
        exporter = TableToHTMLExporter(cells)
        result = exporter.export()

        expected_result = ET.fromstring(
            """<table><tr><td rowspan="2">0</td><td>1</td><td>2</td><td>3</td></tr><tr><td colspan="2">4</td><td>5</td></tr><tr><td>6</td><td rowspan="2">7</td><td>8</td><td>9</td></tr><tr><td>10</td><td colspan="2">11</td></tr></table>""")
        self.assertTrue(self._are_elements_equal(result, expected_result))

    def _are_elements_equal(self, e1, e2):
        if e1.tag != e2.tag: 
            return False
        if e1.text != e2.text: 
            return False
        if e1.tail != e2.tail: 
            return False
        if e1.attrib != e2.attrib: 
            return False
        if len(e1) != len(e2): 
            return False
        return all(self._are_elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

if __name__ == '__main__':
    main()