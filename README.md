# NWBQtGUI
Qt graphical user interface for NWB:

* Customized metadata curation before conversion with [nwb-conversion-tools](https://github.com/catalystneuro/nwb-conversion-tools)
* NWB file explorer with [nwb-widgets](https://github.com/NeurodataWithoutBorders/nwb-jupyter-widgets)

![](images/gif_gui0.gif)

## Installation
To install **NWBQtGUI** directly in an existing environment:
```
$ pip install nwb-qt-gui
```

## GUI
**NWBQtGUI** provides an user-friendly way of editing metafiles for the conversion tasks and for exploring nwb files with [nwb-jupyter-widgets](https://github.com/NeurodataWithoutBorders/nwb-jupyter-widgets) and an embedded IPython console.

After activating the correct environment, NWBQtGUI can be called from command line:
```shell
nwb-gui
```

To initiate the GUI with a specific metafile:
```shell
nwb-gui metafile.yml
```

The GUI can also be imported and run from python scripts:
```python
from nwb_qt_gui.gui import nwb_qt_gui

# YAML metafile
metafile = 'metafile.yml'

# Conversion module
conversion_module = 'conversion_module.py'

# Source files path
source_paths = {}
source_paths['source_file_1'] = {'type': 'file', 'path': ''}
source_paths['source_file_2'] = {'type': 'file', 'path': ''}

# Other options
kwargs = {'option_1': True, 'option_2': False}

nwb_qt_gui(
    metafile=metafile,
    conversion_module=conversion_module,
    source_paths=source_paths,
    kwargs_fields=kwargs,
)
```
