from unittest import TestCase, main

import os
# Turn off tensorflow warnings.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import context
from tables_extractor.page_objects_creator import PageObjectsCreator
from tables_extractor.tables_extractor import TablesExtractor


class TablesExtractorTestCase(TestCase):
    def test_single_table(self):
        page_objects_creator = PageObjectsCreator()
        page_objects_list = page_objects_creator.create_from_path('tests/data/page_28.pdf')
        
        self.assertEqual(len(page_objects_list), 1)
        page_objects = page_objects_list[0]

        tables_extractor = TablesExtractor(page_objects)
        tables = tables_extractor.extract()

        self.assertEqual(len(tables), 1)
        table = tables[0]

        grid_structure = table.grid_structure
        self.assertEqual(grid_structure.get_rows_count(), 4)
        self.assertEqual(grid_structure.get_cols_count(), 4)

        cells = table.cells
        self.assertEqual(len(cells), 16)

        self.assertEqual(cells[0].text, '')
        self.assertEqual(cells[1].text, '2017')
        self.assertEqual(cells[2].text, '2016')
        self.assertEqual(cells[3].text, '2015')

        self.assertEqual(cells[4].text, 'Low')
        self.assertEqual(cells[5].text, '3.25%')
        self.assertEqual(cells[6].text, '2.75%')
        self.assertEqual(cells[7].text, '4.50%')

        self.assertEqual(cells[8].text, 'High')
        self.assertEqual(cells[9].text, '4.50')
        self.assertEqual(cells[10].text, '4.50')
        self.assertEqual(cells[11].text, '7.00')

        self.assertEqual(cells[12].text, 'Weighted-average')
        self.assertEqual(cells[13].text, '4.03')
        self.assertEqual(cells[14].text, '3.82')
        self.assertEqual(cells[15].text, '5.90')


if __name__ == '__main__':
    main()