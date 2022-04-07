import argparse
import xml.etree.ElementTree as ET

from tables_extractor.page_objects_creator import PageObjectsCreator
from tables_extractor.tables_extractor import TablesExtractor
from tables_extractor.table_to_html_exporter import TableToHTMLExporter


def main(args):
    page_objects_list = PageObjectsCreator().create_from_path(args.src_file_path)

    root = ET.Element('html')

    for page_objects in page_objects_list:
        tables = TablesExtractor(page_objects).extract()
        for idx, table in enumerate(tables, start=1):
            table_exporter = TableToHTMLExporter(table.cells)
            table_element = table_exporter.export()
            title_element = ET.SubElement(root, 'h2')
            title_element.text = 'Table {}'.format(idx)
            
            root.append(table_element)

    ET.ElementTree(root).write(args.dst_file_path, encoding='utf-8', method='html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Exports tables from pdf document to html format.")
    parser.add_argument('src_file_path', help='Path to source pdf file.')
    parser.add_argument('dst_file_path', help='Path to destination html file.')

    main(parser.parse_args())