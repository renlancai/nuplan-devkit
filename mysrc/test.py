from bokeh.io import output_notebook
from tutorials.utils.tutorial_utils import visualize_nuplan_scenarios, setup_notebook


setup_notebook()
output_notebook()

import os

NUPALN_DATASET = "/home/tsai/nuplan/dataset/"

NUPLAN_DATA_ROOT = os.getenv('NUPLAN_DATA_ROOT', NUPALN_DATASET)
NUPLAN_MAPS_ROOT = os.getenv('NUPLAN_MAPS_ROOT', NUPALN_DATASET + '/maps')
NUPLAN_DB_FILES = os.getenv('NUPLAN_DB_FILES', NUPALN_DATASET + '/nuplan-v1.1/splits/mini')
NUPLAN_MAP_VERSION = os.getenv('NUPLAN_MAP_VERSION', 'nuplan-maps-v1.0')


visualize_nuplan_scenarios(
    data_root=NUPLAN_DATA_ROOT,
    db_files=NUPLAN_DB_FILES,
    map_root=NUPLAN_MAPS_ROOT,
    map_version=NUPLAN_MAP_VERSION,
    bokeh_port=8899  # This controls the port bokeh uses when generating the visualization -- if you are running
                     # the notebook on a remote instance, you'll need to make sure to port-forward it.
)
