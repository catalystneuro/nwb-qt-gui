from PySide2.QtWidgets import (QLineEdit, QVBoxLayout, QGridLayout, QLabel,
                               QGroupBox, QComboBox, QCheckBox, QMessageBox)
from nwb_qt_gui.utils.configs import required_asterisk_color
from nwb_qt_gui.classes.forms_general import GroupDevice
from nwb_qt_gui.classes.forms_misc import GroupDecompositionSeries
from nwb_qt_gui.classes.collapsible_box import CollapsibleBox
from nwb_qt_gui.classes.forms_basic import BasicFormCollapsible
import pynwb
from itertools import groupby


class GroupElectrodeGroup(BasicFormCollapsible):
    def __init__(self, parent, metadata=None):
        """Groupbox for pynwb.ecephys.ElectrodeGroup fields filling form."""
        super().__init__(parent=parent, pynwb_class=pynwb.ecephys.ElectrodeGroup, metadata=metadata)

    def fields_info_update(self):
        """Updates fields info with specific fields from the inheriting class."""
        specific_fields = [
            {'name': 'device',
             'type': 'link',
             'class': 'Device',
             'required': True,
             'doc': 'The device that was used to record'},
        ]
        self.fields_info.extend(specific_fields)


class GroupElectricalSeries(CollapsibleBox):
    def __init__(self, parent):
        """Groupbox for pynwb.ecephys.ElectricalSeries fields filling form."""
        super().__init__(title="ElectricalSeries", parent=parent)
        self.parent = parent
        self.group_type = 'ElectricalSeries'

        self.lbl_name = QLabel('name<span style="color:' + required_asterisk_color + ';">*</span>:')
        self.form_name = QLineEdit('ElectricalSeries')
        self.form_name.setToolTip("The unique name of this ElectricalSeries dataset.")

        self.lbl_electrodes = QLabel('electrodes<span style="color:' + required_asterisk_color + ';">*</span>:')
        self.chk_electrodes = QCheckBox("Get from source file")
        self.chk_electrodes.setChecked(True)
        self.chk_electrodes.setToolTip(
            "The table region corresponding to the electrodes "
            "from which this series was recorded.\n"
            "Check box if this data will be retrieved from source file.\n"
            "Uncheck box to ignore it.")

        self.lbl_conversion = QLabel('conversion:')
        self.form_conversion = QLineEdit('')
        self.form_conversion.setPlaceholderText("1.0")
        self.form_conversion.setToolTip("Scalar to multiply each element by to convert to volts")

        self.lbl_resolution = QLabel('resolution:')
        self.form_resolution = QLineEdit('')
        self.form_resolution.setToolTip(
            "The smallest meaningful difference (in specified unit) between values in data")

        self.lbl_timestamps = QLabel('timestamps:')
        self.chk_timestamps = QCheckBox("Get from source file")
        self.chk_timestamps.setChecked(False)
        self.chk_timestamps.setToolTip(
            "Timestamps for samples stored in data.\n"
            "Check box if this data will be retrieved from source file.\n"
            "Uncheck box to ignore it.")

        self.lbl_starting_time = QLabel('starting_time:')
        self.form_starting_time = QLineEdit('')
        self.form_starting_time.setPlaceholderText("0.0")
        self.form_starting_time.setToolTip("The timestamp of the first sample")

        self.lbl_rate = QLabel('rate:')
        self.form_rate = QLineEdit('')
        self.form_rate.setPlaceholderText("0.0")
        self.form_rate.setToolTip("Sampling rate in Hz")

        self.lbl_comments = QLabel('comments:')
        self.form_comments = QLineEdit('')
        self.form_comments.setPlaceholderText("comments")
        self.form_comments.setToolTip("Human-readable comments about this ElectricalSeries dataset")

        self.lbl_description = QLabel('description:')
        self.form_description = QLineEdit('')
        self.form_description.setPlaceholderText("description")
        self.form_description.setToolTip(" Description of this ElectricalSeries dataset")

        self.grid = QGridLayout()
        self.grid.setColumnStretch(4, 1)
        self.grid.addWidget(self.lbl_name, 0, 0, 1, 2)
        self.grid.addWidget(self.form_name, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_electrodes, 2, 0, 1, 2)
        self.grid.addWidget(self.chk_electrodes, 2, 2, 1, 2)
        self.grid.addWidget(self.lbl_conversion, 3, 0, 1, 2)
        self.grid.addWidget(self.form_conversion, 3, 2, 1, 4)
        self.grid.addWidget(self.lbl_resolution, 4, 0, 1, 2)
        self.grid.addWidget(self.form_resolution, 4, 2, 1, 4)
        self.grid.addWidget(self.lbl_timestamps, 5, 0, 1, 2)
        self.grid.addWidget(self.chk_timestamps, 5, 2, 1, 2)
        self.grid.addWidget(self.lbl_starting_time, 6, 0, 1, 2)
        self.grid.addWidget(self.form_starting_time, 6, 2, 1, 4)
        self.grid.addWidget(self.lbl_rate, 7, 0, 1, 2)
        self.grid.addWidget(self.form_rate, 7, 2, 1, 4)
        self.grid.addWidget(self.lbl_comments, 8, 0, 1, 2)
        self.grid.addWidget(self.form_comments, 8, 2, 1, 4)
        self.grid.addWidget(self.lbl_description, 9, 0, 1, 2)
        self.grid.addWidget(self.form_description, 9, 2, 1, 4)
        self.setContentLayout(self.grid)

    def refresh_objects_references(self, metadata=None):
        """Refreshes references with existing objects in parent group."""
        pass

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['name'] = self.form_name.text()
        if self.chk_electrodes.isChecked():
            data['electrodes'] = True
        try:
            data['conversion'] = float(self.form_conversion.text())
        except ValueError as error:
            print(error)
        try:
            data['resolution'] = float(self.form_resolution.text())
        except ValueError as error:
            print(error)
        if self.chk_timestamps.isChecked():
            data['timestamps'] = True
        try:
            data['starting_time'] = float(self.form_starting_time.text())
        except ValueError as error:
            print(error)
        try:
            data['rate'] = float(self.form_rate.text())
        except ValueError as error:
            print(error)
        data['comments'] = self.form_comments.text()
        data['description'] = self.form_description.text()
        return data

    def write_fields(self, metadata={}):
        """Reads structured dictionary and write in form fields."""
        self.form_name.setText(metadata['name'])
        self.chk_electrodes.setChecked(True)
        if 'conversion' in metadata:
            self.form_conversion.setText(str(metadata['conversion']))
        if 'resolution' in metadata:
            self.form_resolution.setText(str(metadata['resolution']))
        if 'timestamps' in metadata:
            self.chk_timestamps.setChecked(True)
        if 'starting_time' in metadata:
            self.form_starting_time.setText(str(metadata['starting_time']))
        if 'rate' in metadata:
            self.form_rate.setText(str(metadata['rate']))
        if 'comments' in metadata:
            self.form_comments.setText(metadata['comments'])
        if 'description' in metadata:
            self.form_description.setText(metadata['description'])


class GroupSpikeEventSeries(QGroupBox):
    def __init__(self, parent):
        """Groupbox for pynwb.ecephys.SpikeEventSeries fields filling form."""
        super().__init__()
        self.setTitle('SpikeEventSeries')
        self.parent = parent
        self.group_type = 'SpikeEventSeries'

        self.lbl_name = QLabel('name<span style="color:' + required_asterisk_color + ';">*</span>:')
        self.form_name = QLineEdit('SpikeEventSeries')
        self.form_name.setToolTip("The unique name of this SpikeEventSeries.")

        self.lbl_timestamps = QLabel('timestamps<span style="color:' + required_asterisk_color + ';">*</span>:')
        self.chk_timestamps = QCheckBox("Get from source file")
        self.chk_timestamps.setChecked(True)
        self.chk_timestamps.setToolTip(
            "Timestamps for samples stored in data.\n"
            "Check box if this data will be retrieved from source file.\n"
            "Uncheck box to ignore it.")

        self.lbl_electrodes = QLabel('electrodes<span style="color:' + required_asterisk_color + ';">*</span>:')
        self.chk_electrodes = QCheckBox("Get from source file")
        self.chk_electrodes.setChecked(True)
        self.chk_electrodes.setToolTip(
            "The table region corresponding to the electrodes from which this series was recorded.\n"
            "Check box if this data will be retrieved from source file.\n"
            "Uncheck box to ignore it.")

        self.lbl_conversion = QLabel('conversion:')
        self.form_conversion = QLineEdit('')
        self.form_conversion.setPlaceholderText("1.0")
        self.form_conversion.setToolTip("Scalar to multiply each element by to convert to volts")

        self.lbl_resolution = QLabel('resolution:')
        self.form_resolution = QLineEdit('')
        self.form_resolution.setPlaceholderText("1.0")
        self.form_resolution.setToolTip(
            "The smallest meaningful difference (in specified unit) between values in data")

        self.lbl_comments = QLabel('comments:')
        self.form_comments = QLineEdit('')
        self.form_comments.setPlaceholderText("comments")
        self.form_comments.setToolTip("Human-readable comments about this SpikeEventSeries dataset")

        self.lbl_description = QLabel('description:')
        self.form_description = QLineEdit('')
        self.form_description.setPlaceholderText("description")
        self.form_description.setToolTip(" Description of this SpikeEventSeries dataset")

        self.grid = QGridLayout()
        self.grid.setColumnStretch(4, 1)
        self.grid.addWidget(self.lbl_name, 0, 0, 1, 2)
        self.grid.addWidget(self.form_name, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_timestamps, 2, 0, 1, 2)
        self.grid.addWidget(self.chk_timestamps, 2, 2, 1, 2)
        self.grid.addWidget(self.lbl_electrodes, 3, 0, 1, 2)
        self.grid.addWidget(self.chk_electrodes, 3, 2, 1, 2)
        self.grid.addWidget(self.lbl_conversion, 4, 0, 1, 2)
        self.grid.addWidget(self.form_conversion, 4, 2, 1, 4)
        self.grid.addWidget(self.lbl_resolution, 5, 0, 1, 2)
        self.grid.addWidget(self.form_resolution, 5, 2, 1, 4)
        self.grid.addWidget(self.lbl_comments, 8, 0, 1, 2)
        self.grid.addWidget(self.form_comments, 8, 2, 1, 4)
        self.grid.addWidget(self.lbl_description, 9, 0, 1, 2)
        self.grid.addWidget(self.form_description, 9, 2, 1, 4)
        self.setLayout(self.grid)

    def refresh_objects_references(self, metadata=None):
        """Refreshes references with existing objects in parent group."""
        pass

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['name'] = self.form_name.text()
        if self.chk_electrodes.isChecked():
            data['electrodes'] = True
        try:
            data['conversion'] = float(self.form_conversion.text())
        except ValueError as error:
            print(error)
        try:
            data['resolution'] = float(self.form_resolution.text())
        except ValueError as error:
            print(error)
        if self.chk_timestamps.isChecked():
            data['timestamps'] = True
        data['comments'] = self.form_comments.text()
        data['description'] = self.form_description.text()
        return data

    def write_fields(self, metadata={}):
        """Reads structured dictionary and write in form fields."""
        self.form_name.setText(metadata['name'])
        self.chk_timestamps.setChecked(True)
        self.chk_electrodes.setChecked(True)
        if 'conversion' in metadata:
            self.form_conversion.setText(str(metadata['conversion']))
        if 'resolution' in metadata:
            self.form_resolution.setText(str(metadata['resolution']))
        if 'comments' in metadata:
            self.form_comments.setText(metadata['comments'])
        if 'description' in metadata:
            self.form_description.setText(metadata['description'])


class GroupEventDetection(QGroupBox):
    def __init__(self, parent):
        """Groupbox for pynwb.ecephys.EventDetection fields filling form."""
        super().__init__()
        self.setTitle('EventDetection')
        self.parent = parent
        self.group_type = 'EventDetection'

        self.lbl_name = QLabel('name<span style="color:'+required_asterisk_color+';">*</span>:')
        self.form_name = QLineEdit('EventDetection')
        self.form_name.setToolTip("The unique name of this EventDetection")
        nInstances = 0
        for grp in self.parent.groups_list:
            if isinstance(grp,  GroupEventDetection):
                nInstances += 1
        if nInstances > 0:
            self.form_name.setText('EventDetection'+str(nInstances))

        self.lbl_detection_method = QLabel('detection_method<span style="color:'+required_asterisk_color+';">*</span>:')
        self.form_detection_method = QLineEdit('detection_method')
        self.form_detection_method.setToolTip(
            "Description of how events were detected, such as voltage threshold, "
            "or dV/dT threshold, as well as relevant values")

        self.lbl_source_electricalseries = QLabel('source_electricalseries<span style="color:'+required_asterisk_color+';">*</span>:')
        self.combo_source_electricalseries = CustomComboBox()
        self.combo_source_electricalseries.setToolTip("The source electrophysiology data")

        self.lbl_source_idx = QLabel('source_idx<span style="color:'+required_asterisk_color+';">*</span>:')
        self.chk_source_idx = QCheckBox("Get from source file")
        self.chk_source_idx.setChecked(True)
        self.chk_source_idx.setToolTip(
            "Indices (zero-based) into source ElectricalSeries "
            "data array corresponding to time of event. \nModule description should define "
            "what is meant by time of event (e.g., .25msec before action potential peak, \n"
            "zero-crossing time, etc). The index points to each event from the raw data.\n"
            "Check box if this data will be retrieved from source file.\n"
            "Uncheck box to ignore it.")

        self.lbl_times = QLabel('times<span style="color:'+required_asterisk_color+';">*</span>:')
        self.chk_times = QCheckBox("Get from source file")
        self.chk_times.setChecked(True)
        self.chk_times.setToolTip(
            "Timestamps of events, in Seconds.\n"
            "Check box if this data will be retrieved from source file.\n"
            "Uncheck box to ignore it.")

        self.grid = QGridLayout()
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lbl_name, 0, 0, 1, 2)
        self.grid.addWidget(self.form_name, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_detection_method, 1, 0, 1, 2)
        self.grid.addWidget(self.form_detection_method, 1, 2, 1, 4)
        self.grid.addWidget(self.lbl_source_electricalseries, 2, 0, 1, 2)
        self.grid.addWidget(self.combo_source_electricalseries, 2, 2, 1, 4)
        self.grid.addWidget(self.lbl_source_idx, 3, 0, 1, 2)
        self.grid.addWidget(self.chk_source_idx, 3, 2, 1, 2)
        self.grid.addWidget(self.lbl_times, 4, 0, 1, 2)
        self.grid.addWidget(self.chk_times, 4, 2, 1, 2)
        self.setLayout(self.grid)

    def refresh_objects_references(self, metadata=None):
        """Refreshes references with existing objects in parent group."""
        self.combo_source_electricalseries.clear()
        for grp in self.parent.groups_list:
            if isinstance(grp, GroupElectricalSeries):
                self.combo_source_electricalseries.addItem(grp.form_name.text())

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['name'] = self.form_name.text()
        data['detection_method'] = self.form_detection_method.text()
        data['source_electricalseries'] = self.combo_source_electricalseries.currentText()
        if self.chk_source_idx.isChecked():
            data['source_idx'] = True
        if self.chk_times.isChecked():
            data['times'] = True
        return data

    def write_fields(self, metadata={}):
        """Reads structured dictionary and write in form fields."""
        self.form_name.setText(metadata['name'])
        self.form_detection_method.setText(metadata['detection_method'])
        self.combo_source_electricalseries.clear()
        self.combo_source_electricalseries.addItem(metadata['source_electricalseries'])
        self.chk_source_idx.setChecked(True)
        self.chk_times.setChecked(True)


class GroupEventWaveform(QGroupBox):
    def __init__(self, parent):
        """Groupbox for pynwb.ecephys.EventWaveform fields filling form."""
        super().__init__()
        self.setTitle('EventWaveform')
        self.parent = parent
        self.group_type = 'EventWaveform'

        self.lbl_name = QLabel('name<span style="color:'+required_asterisk_color+';">*</span>:')
        self.form_name = QLineEdit('EventWaveform')
        self.form_name.setToolTip("The unique name of this EventWaveform")
        nInstances = 0
        for grp in self.parent.groups_list:
            if isinstance(grp,  GroupEventWaveform):
                nInstances += 1
        if nInstances > 0:
            self.form_name.setText('EventWaveform'+str(nInstances))

        self.lbl_spike_event_series = QLabel('spike_event_series<span style="color:'+required_asterisk_color+';">*</span>:')
        self.combo_spike_event_series = CustomComboBox()
        self.combo_spike_event_series.setToolTip("SpikeEventSeries to store in this interface")

        self.grid = QGridLayout()
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lbl_name, 0, 0, 1, 2)
        self.grid.addWidget(self.form_name, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_spike_event_series, 1, 0, 1, 2)
        self.grid.addWidget(self.combo_spike_event_series, 1, 2, 1, 4)
        self.setLayout(self.grid)

    def refresh_objects_references(self, metadata=None):
        """Refreshes references with existing objects in parent group."""
        self.combo_spike_event_series.clear()
        for grp in self.parent.groups_list:
            if isinstance(grp, GroupSpikeEventSeries):
                self.combo_spike_event_series.addItem(grp.form_name.text())

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['name'] = self.form_name.text()
        data['spike_event_series'] = self.combo_spike_event_series.currentText()
        return data

    def write_fields(self, metadata={}):
        """Reads structured dictionary and write in form fields."""
        self.form_name.setText(metadata['name'])
        self.combo_spike_event_series.clear()
        self.combo_spike_event_series.addItem(metadata['spike_event_series'])


class GroupLFP(QGroupBox):
    def __init__(self, parent):
        """Groupbox for pynwb.ecephys.LFP fields filling form."""
        super().__init__()
        self.setTitle('LFP')
        self.parent = parent
        self.group_type = 'LFP'

        self.lbl_name = QLabel('name<span style="color:'+required_asterisk_color+';">*</span>:')
        self.form_name = QLineEdit('LFP')
        self.form_name.setToolTip("The unique name of this LFP")
        nInstances = 0
        for grp in self.parent.groups_list:
            if isinstance(grp,  GroupLFP):
                nInstances += 1
        if nInstances > 0:
            self.form_name.setText('LFP'+str(nInstances))

        self.lbl_electrical_series = QLabel('electrical_series<span style="color:'+required_asterisk_color+';">*</span>:')
        self.electrical_series = GroupElectricalSeries(self)

        self.lbl_decomposition_series = QLabel('decomposition_series<span style="color:'+required_asterisk_color+';">*</span>:')
        self.decomposition_series = GroupDecompositionSeries(self)

        self.grid = QGridLayout()
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lbl_name, 0, 0, 1, 2)
        self.grid.addWidget(self.form_name, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_electrical_series, 1, 0, 1, 2)
        self.grid.addWidget(self.electrical_series, 1, 2, 1, 4)
        self.grid.addWidget(self.lbl_decomposition_series, 2, 0, 1, 2)
        self.grid.addWidget(self.decomposition_series, 2, 2, 1, 4)
        self.setLayout(self.grid)

    def refresh_objects_references(self, metadata=None):
        """Refreshes references with existing objects in parent group."""
        pass

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['name'] = self.form_name.text()
        data['electrical_series'] = self.electrical_series.read_fields()
        data['decomposition_series'] = self.decomposition_series.read_fields()
        return data

    def write_fields(self, metadata={}):
        """Reads structured dictionary and write in form fields."""
        self.form_name.setText(metadata['name'])


class GroupFilteredEphys(QGroupBox):
    def __init__(self, parent):
        """Groupbox for pynwb.ecephys.FilteredEphys fields filling form."""
        super().__init__()
        self.setTitle('FilteredEphys')
        self.parent = parent
        self.group_type = 'FilteredEphys'

        self.lbl_name = QLabel('name<span style="color:'+required_asterisk_color+';">*</span>:')
        self.form_name = QLineEdit('FilteredEphys')
        self.form_name.setToolTip("The unique name of this FilteredEphys")
        nInstances = 0
        for grp in self.parent.groups_list:
            if isinstance(grp,  GroupFilteredEphys):
                nInstances += 1
        if nInstances > 0:
            self.form_name.setText('FilteredEphys'+str(nInstances))

        self.lbl_electrical_series = QLabel('electrical_series<span style="color:'+required_asterisk_color+';">*</span>:')
        self.electrical_series = GroupElectricalSeries(self)

        self.grid = QGridLayout()
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lbl_name, 0, 0, 1, 2)
        self.grid.addWidget(self.form_name, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_electrical_series, 1, 0, 1, 2)
        self.grid.addWidget(self.electrical_series, 1, 2, 1, 4)
        self.setLayout(self.grid)

    def refresh_objects_references(self, metadata=None):
        """Refreshes references with existing objects in parent group."""
        pass

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['name'] = self.form_name.text()
        data['electrical_series'] = self.electrical_series.read_fields()
        return data

    def write_fields(self, metadata={}):
        """Reads structured dictionary and write in form fields."""
        self.form_name.setText(data['name'])
        # self.combo_electrical_series.clear()
        # self.combo_electrical_series.addItem(data['electrical_series'])


class GroupFeatureExtraction(QGroupBox):
    def __init__(self, parent):
        """Groupbox for pynwb.ecephys.FeatureExtraction fields filling form."""
        super().__init__()
        self.setTitle('FeatureExtraction')
        self.parent = parent
        self.group_type = 'FeatureExtraction'

        self.lbl_name = QLabel('name<span style="color:'+required_asterisk_color+';">*</span>:')
        self.form_name = QLineEdit('FeatureExtraction')
        self.form_name.setToolTip("The unique name of this FeatureExtraction")
        nInstances = 0
        for grp in self.parent.groups_list:
            if isinstance(grp,  GroupFeatureExtraction):
                nInstances += 1
        if nInstances > 0:
            self.form_name.setText('FeatureExtraction'+str(nInstances))

        self.lbl_electrodes = QLabel('electrodes<span style="color:'+required_asterisk_color+';">*</span>:')
        self.chk_electrodes = QCheckBox("Get from source file")
        self.chk_electrodes.setChecked(True)
        self.chk_electrodes.setToolTip(
            "The table region corresponding to the electrodes from which this series was recorded.\n"
            "Check box if this data will be retrieved from source file.\n"
            "Uncheck box to ignore it.")

        self.lbl_description = QLabel('description<span style="color:'+required_asterisk_color+';">*</span>:')
        self.form_description = QLineEdit('')
        self.form_description.setToolTip("A description for each feature extracted")

        self.lbl_times = QLabel('times<span style="color:'+required_asterisk_color+';">*</span>:')
        self.chk_times = QCheckBox("Get from source file")
        self.chk_times.setChecked(True)
        self.chk_times.setToolTip(
            "The times of events that features correspond to.\n"
            "Check box if this data will be retrieved from source file.\n"
            "Uncheck box to ignore it.")

        self.lbl_features = QLabel('features<span style="color:'+required_asterisk_color+';">*</span>:')
        self.chk_features = QCheckBox("Get from source file")
        self.chk_features.setChecked(True)
        self.chk_features.setToolTip(
            "Features for each channel.\n"
            "Check box if this data will be retrieved from source file.\n"
            "Uncheck box to ignore it.")

        self.grid = QGridLayout()
        self.grid.setColumnStretch(2, 1)
        self.grid.addWidget(self.lbl_name, 0, 0, 1, 2)
        self.grid.addWidget(self.form_name, 0, 2, 1, 4)
        self.grid.addWidget(self.lbl_electrodes, 1, 0, 1, 2)
        self.grid.addWidget(self.chk_electrodes, 1, 2, 1, 2)
        self.grid.addWidget(self.lbl_description, 2, 0, 1, 2)
        self.grid.addWidget(self.form_description, 2, 2, 1, 4)
        self.grid.addWidget(self.lbl_times, 3, 0, 1, 2)
        self.grid.addWidget(self.chk_times, 3, 2, 1, 2)
        self.grid.addWidget(self.lbl_features, 4, 0, 1, 2)
        self.grid.addWidget(self.chk_features, 4, 2, 1, 2)
        self.setLayout(self.grid)

    def refresh_objects_references(self, metadata=None):
        """Refreshes references with existing objects in parent group."""
        pass

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        data = {}
        data['name'] = self.form_name.text()
        if self.chk_electrodes.isChecked():
            data['electrodes'] = True
        data['description'] = self.form_description.text()
        if self.chk_times.isChecked():
            data['times'] = True
        if self.chk_features.isChecked():
            data['features'] = True
        return data

    def write_fields(self, metadata={}):
        """Reads structured dictionary and write in form fields."""
        self.form_name.setText(metadata['name'])
        self.chk_electrodes.setChecked(True)
        self.form_description.setText(metadata['description'])
        self.chk_times.setChecked(True)
        self.chk_features.setChecked(True)


class GroupEcephys(QGroupBox):
    def __init__(self, parent):
        """Groupbox for Ecephys module fields filling form."""
        super().__init__()
        self.setTitle('Ecephys')
        self.group_type = 'Ecephys'
        self.groups_list = []

        self.combo1 = CustomComboBox()
        self.combo1.addItem('-- Add group --')
        self.combo1.addItem('Device')
        self.combo1.addItem('ElectrodeGroup')
        self.combo1.addItem('ElectricalSeries')
        self.combo1.addItem('SpikeEventSeries')
        self.combo1.addItem('EventDetection')
        self.combo1.addItem('EventWaveform')
        self.combo1.addItem('LFP')
        self.combo1.addItem('FilteredEphys')
        self.combo1.addItem('FeatureExtraction')
        self.combo1.addItem('DecompositionSeries')
        self.combo1.setCurrentIndex(0)
        self.combo1.activated.connect(lambda: self.add_group('combo'))
        self.combo2 = CustomComboBox()
        self.combo2.addItem('-- Del group --')
        self.combo2.setCurrentIndex(0)
        self.combo2.activated.connect(lambda: self.del_group('combo'))

        self.vbox1 = QVBoxLayout()
        self.vbox1.addStretch()

        self.grid = QGridLayout()
        self.grid.setColumnStretch(5, 1)
        if parent.show_add_del:
            self.grid.addWidget(self.combo1, 1, 0, 1, 2)
            self.grid.addWidget(self.combo2, 1, 2, 1, 2)
        self.grid.addLayout(self.vbox1, 2, 0, 1, 6)
        self.setLayout(self.grid)

    def add_group(self, group, metadata=None):
        """Adds group form."""
        if metadata is not None:
            group.write_fields(metadata=metadata)
        group.form_name.textChanged.connect(self.refresh_del_combo)
        self.groups_list.append(group)
        nWidgetsVbox = self.vbox1.count()
        self.vbox1.insertWidget(nWidgetsVbox-1, group)  # insert before the stretch
        self.combo1.setCurrentIndex(0)
        self.combo2.addItem(group.form_name.text())
        self.refresh_children(metadata=metadata)

    def del_group(self, group_name):
        """Deletes group form by name."""
        if group_name == 'combo':
            group_name = str(self.combo2.currentText())
        if group_name != '-- Del group --':
            # Tests if any other group references this one
            if self.is_referenced(grp_unique_name=group_name):
                QMessageBox.warning(self, "Cannot delete subgroup",
                                    group_name+" is being referenced by another subgroup(s).\n"
                                    "You should remove any references of "+group_name+" before "
                                    "deleting it!")
                self.combo2.setCurrentIndex(0)
            else:
                nWidgetsVbox = self.vbox1.count()
                for i in range(nWidgetsVbox):
                    if self.vbox1.itemAt(i) is not None:
                        if hasattr(self.vbox1.itemAt(i).widget(), 'form_name'):
                            if self.vbox1.itemAt(i).widget().form_name.text() == group_name:
                                self.groups_list.remove(self.vbox1.itemAt(i).widget())   # deletes list item
                                self.vbox1.itemAt(i).widget().setParent(None)            # deletes widget
                                self.combo2.removeItem(self.combo2.findText(group_name))
                                self.combo2.setCurrentIndex(0)
                                self.refresh_children()

    def is_referenced(self, grp_unique_name):
        """Tests if a group is being referenced any other groups. Returns boolean."""
        nWidgetsVbox = self.vbox1.count()
        for i in range(nWidgetsVbox):
            if self.vbox1.itemAt(i).widget() is not None:
                other_grp = self.vbox1.itemAt(i).widget()
                # check if this subgroup has any ComboBox referencing grp_unique_name
                for ch in other_grp.children():
                    if isinstance(ch, (CustomComboBox, QComboBox)):
                        if ch.currentText() == grp_unique_name:
                            return True
        return False

    def refresh_children(self, metadata=None):
        """Refreshes references with existing objects in child groups."""
        for child in self.groups_list:
            child.refresh_objects_references(metadata=metadata)

    def refresh_del_combo(self):
        """Refreshes del combobox with existing objects names in child groups."""
        self.combo2.clear()
        self.combo2.addItem('-- Del group --')
        for child in self.groups_list:
            self.combo2.addItem(child.form_name.text())
        self.refresh_children()

    def read_fields(self):
        """Reads fields and returns them structured in a dictionary."""
        error = None
        data = {}
        # group_type counts, if there are multiple groups of same type, they are saved in a list
        grp_types = [grp.group_type for grp in self.groups_list]
        grp_type_count = {value: len(list(freq)) for value, freq in groupby(sorted(grp_types))}
        # initiate lists as values for groups keys with count > 1
        for k, v in grp_type_count.items():
            if v > 1 or k == 'Device' or k == 'ElectrodeGroup' or k == 'ElectricalSeries':
                data[k] = []
        # iterate over existing groups and copy their metadata
        for grp in self.groups_list:
            if grp_type_count[grp.group_type] > 1 or grp.group_type == 'Device' \
               or grp.group_type == 'ElectrodeGroup' or grp.group_type == 'ElectricalSeries':
                data[grp.group_type].append(grp.read_fields())
            else:
                data[grp.group_type] = grp.read_fields()
        return data, error


class CustomComboBox(QComboBox):
    def __init__(self):
        """Class created to ignore mouse wheel events on combobox."""
        super().__init__()

    def wheelEvent(self, event):
        event.ignore()
