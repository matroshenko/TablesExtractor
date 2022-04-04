import xml.etree.ElementTree as ET


class TableToHTMLExporter(object):
    def __init__(self, table):
        self._table = table

    def export(self):
        table_element = ET.Element('table')
        row_element = ET.SubElement(table_element, 'tr')

        cells = self._table.cells
        current_row = cells[0].grid_rect.top
        for cell in cells:
            if cell.grid_rect.top > current_row:
                row_element = ET.SubElement(table_element, 'tr')
                current_row = cell.grid_rect.top

            rowspan = cell.grid_rect.get_height()
            colspan = cell.grid_rect.get_width()
            cell_element = ET.SubElement(row_element, 'td')
            if rowspan > 1:
                cell_element['rowspan'] = rowspan
            if colspan > 1:
                cell_element['colspan'] = colspan
            cell_element.text = cell.text
        
        return table_element