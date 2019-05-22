# coding=utf-8
from setuptools import setup

setup(
    name='codding',
    version='0.0.1',
    packages=['src', 'src.GUI', 'src.GUI.windows', 'src.GUI.controller', 'src.coders', 'src.coders.linear',
              'src.coders.cyclical', 'src.coders.fountain', 'src.coders._interleaver', 'src.coders.convolutional',
              'src.helper', 'src.helper.error', 'src.helper.error.exception', 'src.helper.error.exception.GUI',
              'src.channel', 'tests'],
    url='http://github.com/banifest/codding',
    license='MIT',
    author='Aliaksandr Martyniuk',
    author_email='banifest@gmail.com',
    description='Diploma Codding', install_requires=[
        'sqlalchemy', 'alembic', 'matplotlib', 'PyQt5', 'numpy', 'psycopg2', 'jsonpickle',
    ]
)
