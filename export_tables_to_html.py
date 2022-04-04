import argparse
import xml.etree.ElementTree as ET
import os
# Turn off tensorflow warnings.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from page_objects_creator import PageObjectsCreator
from tables_extractor import TablesExtractor
from table_to_html_exporter import TableToHTMLExporter


def main(args):
    page_objects_list = PageObjectsCreator().create(args.src_file_path)

    root = ET.Element('html')

    for page_objects in page_objects_list:
        tables = TablesExtractor(page_objects).extract()
        for table in tables:
            table_element = TableToHTMLExporter(table.cells).export()
            root.append(table_element)

    ET.ElementTree(root).write(args.dst_file_path, encoding='utf-8', method='html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Exports tables from pdf document to html format.")
    parser.add_argument('src_file_path', help='Path to source pdf file.')
    parser.add_argument('dst_file_path', help='Path to destination html file.')

    main(parser.parse_args())