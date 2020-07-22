from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='nwb-qt-gui',
    version='0.1.0',
    description='Qt graphical user interface for NWB conversion and exploring',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ben Dichter and Luiz Tauffer',
    author_email='ben.dichter@gmail.com',
    url='https://github.com/catalystneuro/nwb-qt-gui',
    keywords='nwb',
    packages=find_packages(),
    package_data={'': ['template_metafile.yml']},
    include_package_data=True,
    install_requires=[
        'pynwb', 'tqdm', 'natsort', 'numpy', 'scipy',
        'pandas', 'jupyter', 'matplotlib', 'h5py', 'pyyaml', 'jupyter-client',
        'PySide2', 'nwbwidgets', 'psutil', 'voila'
    ],
    entry_points={
        'console_scripts': ['nwb-gui=nwb_qt_gui.command_line:main'],
    }
)
