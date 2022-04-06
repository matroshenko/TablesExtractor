from setuptools import setup

setup(
    name='TablesExtractor',
    version='0.1',
    packages=['tables_extractor'],
    install_requires=[
        'Pillow==9.0.1',
        'tensorflow==2.8.0',
        'pymupdf==1.19.6'
    ]
)