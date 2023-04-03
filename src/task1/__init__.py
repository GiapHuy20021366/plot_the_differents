from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f)
           and not f.endswith('__init__.py')]


class Levels:
    CHANGE_RECT_COLOR = "CHAN_RECT_COLOR"
    FLIP_RECT = "FLIP_RECT"
    CHANGE_EDGES_COLOR = "CHANGE_EDGES_COLOR"
    CHANGE_COLOR_REGIONS = "CHANGE_COLOR_REGIONS"
    ERASE_REGIONS = "ERASE_REGIONS"
