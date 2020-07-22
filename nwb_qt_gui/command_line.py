# Coomand line shortcurt to open NWBQtGUI
# authors: Luiz Tauffer and Ben Dichter
# ------------------------------------------------------------------------------
from nwb_qt_gui.gui import nwb_qt_gui
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    metafile = here / 'template_metafile.yml'
    conversion_module = here / 'template_conversion_module.py'

    source_paths = {}
    source_paths['file1'] = {'type': 'file', 'path': ''}
    source_paths['file2'] = {'type': 'file', 'path': ''}

    kwargs_fields = {}

    nwb_qt_gui(
        metafile=metafile,
        conversion_module=conversion_module,
        source_paths=source_paths,
        kwargs_fields=kwargs_fields
    )
