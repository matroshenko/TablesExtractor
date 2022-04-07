from setuptools import setup
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('tables_extractor/models')

setup(
    name='TablesExtractor',
    version='0.1',
    packages=['tables_extractor'],
    package_data={'tables_extractor': extra_files},
    install_requires=[
        'Pillow==9.0.1',
        'tensorflow==2.8.0',
        'pymupdf==1.19.6'
    ]
)