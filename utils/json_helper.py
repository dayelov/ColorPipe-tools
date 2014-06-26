""" json (3D LUT) helpers

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
from utils.abstract_lut_helper import AbstractLUTHelper
import utils.lut_presets as presets
import json


class JsonHelperException(Exception):
    """Module custom exception

    Args:
        Exception

    """
    pass


class JsonLutHelper(AbstractLUTHelper):
    """Json LUT helper

    """
    @staticmethod
    def get_default_preset():
        return {
            presets.TYPE: "3D",
            presets.EXT: ".json",
            presets.IN_RANGE: [0, 1.0],
            presets.OUT_RANGE: [0, 1.0],
            presets.CUBE_SIZE: 17,
            presets.TITLE: "json LUT",
            presets.COMMENT: ("Generated by ColorPipe-tools, "
                              "json_helper {0}").format(__version__),
            presets.VERSION: "1",
            }

    def _write_1d_2d_lut(self, process_function, file_path, preset,
                         line_function):
        message = "1D/2D  LUT is not supported in json format"
        raise JsonHelperException(message)

    def write_3d_lut(self, process_function, file_path, preset):
        in_data, data = self._get_3d_data(process_function, preset)
        cube_size = preset[presets.CUBE_SIZE]
        input_colors = []
        # get input color values
        for rgb in in_data:
            input_colors.append([rgb.r / float(cube_size),
                                 rgb.g / float(cube_size),
                                 rgb.b / float(cube_size)])
        # remap processed values
        red_values = []
        green_values = []
        blue_values = []
        for rgb in data:
            red_values.append(rgb.r)
            green_values.append(rgb.g)
            blue_values.append(rgb.b)
        # create json dict
        json_data = {
            'cubesize': cube_size,
            'red_values': red_values,
            'green_values': green_values,
            'blue_values': blue_values,
            'input_colors': input_colors
            }
        # write data
        lutfile = open(file_path, 'w+')
        json.dump(json_data, lutfile)
        lutfile.close()
        return self.get_export_message(file_path)

    def _validate_preset(self, preset, mode=presets.RAISE_MODE,
                         default_preset=None):
        default_preset = self.get_default_preset()
        # type must be 3D, there's no 1d/2d json
        if presets.TYPE in preset and not preset[presets.TYPE] == '3D':
            if mode == presets.RAISE_MODE:
                raise JsonHelperException(("'{0}' is not a valid type for son "
                                           "LUT. Choose '3D'"
                                           ).format(preset[presets.TYPE]))
            preset[presets.TYPE] = default_preset[presets.TYPE]
        # check basic arguments
        return AbstractLUTHelper._validate_preset(self, preset, mode,
                                                  default_preset)

JSON_HELPER = JsonLutHelper()
