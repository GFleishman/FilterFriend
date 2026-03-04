import numpy as np
import nrrd
import napari
import sys
from magicgui.widgets import PushButton, ComboBox, Container, FloatSpinBox, SpinBox
from psygnal import Signal
from fishspot.filter import percentile_filter, density_filter


# constants
FILTER_TYPES = [
    'Percentile',
    'Density',
]


class filters_widget:

    def __init__(self, viewer):
        self.dock_widget = None
        self.viewer = viewer
        self.filter_menu = ComboBox(label='Filter Type', choices=FILTER_TYPES)
        self.add_filter_button = PushButton(text='Add Filter', tooltip='add filter to end of filter list')
        self.add_filter_button.changed.connect(self._add_filter)
        self.run_filters_button = PushButton(text='Run Filters', tooltip='run current filter stack on current spots')
        self.run_filters_button.changed.connect(self._run_filters)
        self.widgets = [
            self.filter_menu,
            self.add_filter_button,
            self.run_filters_button,
        ]
        self._update_viewer()

    def _add_filter(self):
        filter_type = self.filter_menu.value
        remove = PushButton(text='Remove Filter')
        remove.changed.connect(self._remove_filter)
        if filter_type == 'Percentile':
            percentile = FloatSpinBox(label='percentile', value=0., min=0., max=100., step=1.)
            container = Container(widgets=[percentile, remove,])
        elif filter_type == 'Density':
            radius = FloatSpinBox(label='radius', value=0., min=0., max=1e12, step=0.1)
            num_neighbors = SpinBox(label='neighbor count', value=0, min=0, max=1e12, step=1)
            container = Container(widgets=[radius, num_neighbors, remove,])
        self.widgets.insert(-1, container)
        self._update_viewer()

    def _remove_filter(self):
        sender = Signal.sender()
        for iii, widget in enumerate(self.widgets):
            if isinstance(widget, Container):
                for sub_widget in widget:
                    if sender == sub_widget:
                        self.widgets.pop(iii)
                        break
            else:
                if sender == widget:
                    self.widgets.pop(iii)
                    break
        self._update_viewer()

    def _update_viewer(self):
        if self.dock_widget is not None:
            self.viewer.window.remove_dock_widget(self.dock_widget)
        self.dock_widget = self.viewer.window.add_dock_widget(
            Container(widgets=self.widgets),  # need to make scrollable or deal with layout somehow
            name='filters',
            area='right',
        )

    def _run_filters(self):
        functions = []
        for container in self.widgets[2:-1]:
            if len(container) == 2:
                percentile = container[0].value
                functions.append(lambda x: percentile_filter(x, percentile))
            elif len(container) == 3:
                radius = container[0].value
                num_neighbors = container[1].value
                df = lambda x: density_filter(
                    x, radius, num_neighbors,
                    weight_by_intensity=True,
                    weight_by_size=True,
                )
                functions.append(df)
        filter_spots(functions)


def filter_spots(functions):
    global viewer, original_spots, filtered_points_layer

    # filter the spots
    filtered_spots = np.copy(original_spots)
    for function in functions:
        filtered_spots = function(filtered_spots)

    # replace layer with updated one
    if filtered_points_layer is not None:
        viewer.layers.remove('filtered-spots')
    features = {
        'size-z':filtered_spots[:, 3],
        'size-y':filtered_spots[:, 4],
        'size-x':filtered_spots[:, 5],
        'intensity':filtered_spots[:, 6],
    }
    filtered_points_layer = viewer.add_points(
        data=filtered_spots[:, :3],
        features=features,
        name='filtered-spots',
        ndim=3,
        border_color='transparent',
        face_color='green',
        opacity=0.5,
        symbol='o',
        size=5,
        out_of_slice_display=True,
        blending='additive',
    )
    filtered_points_layer.mode = 'select'


if __name__ == '__main__':

    # print help message
    if isinstance(sys.argv[1], str) and sys.argv[1] in ('-h', '--h', '-help', '--help'):
        print("""
             ~*~~**~~~*** FilterFriend ***~~~**~~*~
        help message
        """)
        sys.exit()

    # load datasets, convert to voxel spacing, make filtering copy
    image, metadata = nrrd.read(sys.argv[1])
    image = image.transpose(2,1,0)
    spacing = np.array(metadata['spacings'])[::-1]
    original_spots = np.loadtxt(sys.argv[2])
    original_spots[:, :3] = np.round(original_spots[:, :3] / spacing).astype(int)

    # instantiate viewer
    viewer = napari.Viewer()

    # add image
    viewer.add_image(
        data=image,
        name='hcr-image',
        blending='additive',
        colormap='gray',
        contrast_limits=[200, 300],
    )

    # add original points layer
    features = {
        'size-z':original_spots[:, 3],
        'size-y':original_spots[:, 4],
        'size-x':original_spots[:, 5],
        'intensity':original_spots[:, 6],
    }
    original_points_layer = viewer.add_points(
        data=original_spots[:, :3],
        features=features,
        name='original-spots',
        ndim=3,
        border_color='transparent',
        face_color='red',
        opacity=0.5,
        symbol='o',
        size=5,
        out_of_slice_display=True,
        blending='additive',
        visible=False,
    )
    original_points_layer.mode = 'select'

    # initialize filtered points layer
    filtered_points_layer = None

    # add filters widget
    filters_widget = filters_widget(viewer)

    # launch napari
    napari.run()
