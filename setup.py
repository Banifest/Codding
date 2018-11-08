from setuptools import setup

setup(
    name='codding',
    version='0.0.1',
    packages=['src', 'src.GUI', 'src.GUI.windows', 'src.GUI.controller', 'src.coders', 'src.coders.linear',
              'src.coders.cyclical', 'src.coders.fountain', 'src.coders.interleaver', 'src.coders.convolutional',
              'src.helper', 'src.helper.error', 'src.helper.error.exception', 'src.helper.error.exception.GUI',
              'src.channel', 'tests'],
    url='',
    license='MIT',
    author='Aliaksandr Martyniuk',
    author_email='banifest@gmail.com',
    description='Diploma'
)
