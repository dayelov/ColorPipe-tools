""" Abstract LUT Helper

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
__version__ = "0.1"
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from numpy import linspace
from utils.lut_utils import get_file_shortname
from utils import lut_presets as presets

# RGB triplet object
Rgb = namedtuple('Rgb', 'r g b')


class AbstractLUTException(Exception):
    """Module custom exception

    """
    pass


class AbstractLUTHelper(object):
    """Abstract LUT helper

    """
    __metaclass__ = ABCMeta

    @staticmethod
    def _get_pattern_1d(preset):
        """ Get string pattern considering sampling types (float / int)

        Args:
            preset (dict): lut generic and sampling informations

        Returns:
            .str

        """
        is_int = AbstractLUTHelper.is_output_int(preset)
        if is_int:
            pattern = "{0}\n"
        else:
            pattern = "{0:.6f}\n"
        return pattern

    @staticmethod
    def _get_pattern(preset):
        """ Get string pattern considering sampling types (float / int)

        Args:
            preset (dict): lut generic and sampling informations

        Returns:
            .str

        """
        is_int = AbstractLUTHelper.is_output_int(preset)
        if is_int:
            pattern = "{0} {1} {2}\n"
        else:
            pattern = "{0:.6f} {1:.6f} {2:.6f}\n"
        return pattern

    def _get_r_value_line(self, preset, rgb):
        """ Get string pattern for a 1D LUT

        Args:
            preset (dict): lut generic and sampling informations

            rgb (Rgb): values

        Returns:
            .str

        """
        return self._get_pattern_1d(preset).format(rgb.r)

    def _get_rgb_value_line(self, preset, rgb):
        """ Get string pattern for a 2D / 3D LUT
        Args:
            preset (dict): lut generic and sampling informations

            rgb Rgb): values

        Returns:
            .str

        """
        return self._get_pattern(preset).format(rgb.r, rgb.g, rgb.b)

    @staticmethod
    def _get_1d_data(processor, preset, preset_helper=presets.PRESET_HELPER):
        """ Process 1D/2D data considering LUT params

        Args:
            processor (PyOpenColorIO.config.Processor): OpenColorIO processor

            preset (dict): lut generic and sampling informations

        Returns:
            .[Rgb]

        """
        preset_helper.check_preset(preset)
        if not preset_helper.is_1d_or_2d_preset(preset):
            raise AbstractLUTException(("Preset isn't valid for 1D / 2D LUT:"
                                        " {0}").format(preset))
        input_range = preset[presets.IN_RANGE]
        output_range = preset[presets.OUT_RANGE]
        samples_count = pow(2,  preset[presets.OUT_BITDEPTH])
        is_int = AbstractLUTHelper.is_output_int(preset)
        compute_range = linspace(input_range[0],
                                      input_range[1],
                                      samples_count)
        data = []
        for code_value in compute_range:
            res = processor.applyRGB([code_value, code_value, code_value])
            res = [(x * output_range[1]) + output_range[0] for x in res]
            if is_int:
                res = [int(x) for x in res]
            data.append(Rgb(res[0], res[1], res[2]))
        return data

    @staticmethod
    def _get_3d_data(processor, preset, preset_helper=presets.PRESET_HELPER):
        """ Process 3D data considering LUT params

        Args:
            processor (PyOpenColorIO.config.Processor): OpenColorIO processor

            preset (dict): lut generic and sampling informations

        Returns:
            .[Rgb]

        """
        preset_helper.check_preset(preset)
        if not preset_helper.is_3d_preset(preset):
            raise AbstractLUTException(("Preset isn't valid for 3D LUT:"
                                        " {0}").format(preset))
        cube_size = preset[presets.CUBE_SIZE]
        input_range = preset[presets.IN_RANGE]
        output_range = preset[presets.OUT_RANGE]
        is_int = False
        if (isinstance(output_range[0], int)
            and isinstance(output_range[1], int)):
            is_int = True
        compute_range = linspace(input_range[0],
                                 input_range[1],
                                 cube_size)
        data = []
        for blue in compute_range:
            for green in compute_range:
                for red in compute_range:
                    res = processor.applyRGB([red, green, blue])
                    res = [(x * output_range[1]) + output_range[0]
                           for x in res]
                    if is_int:
                        res = [int(x) for x in res]
                    data.append(Rgb(res[0], res[1], res[2]))
        return data

    @abstractmethod
    def _write_1d_2d_lut(self, processor, file_path, preset, line_function):
        """ Write 1d / 2d LUT in output file

        Args:
            processor (PyOpenColorIO.config.Processor): OpenColorIO processor

            preset (dict): lut generic and sampling informations

            line_function (function): describe how color values are written.
            Ex: "r g b" or "r, g, b" or "r".
            Use _get_rgb_value_line or _get_r_value_line

        """
        pass

    def write_2d_lut(self, processor, file_path, preset):
        """ Write 2d LUT in output file

        Args:
            processor (PyOpenColorIO.config.Processor): OpenColorIO processor

            preset (dict): lut generic and sampling informations
        """
        self._write_1d_2d_lut(processor, file_path, preset,
                              self._get_rgb_value_line)

    def write_1d_lut(self, processor, file_path, preset):
        """ Write 2d LUT in output file

        Args:
            processor (PyOpenColorIO.config.Processor): OpenColorIO processor

            preset (dict): lut generic and sampling informations
        """
        self._write_1d_2d_lut(processor, file_path, preset,
                              self._get_r_value_line)

    @abstractmethod
    def write_3d_lut(self, processor, file_path, preset):
        """ Write 3d LUT in output file

        Args:
            processor (PyOpenColorIO.config.Processor): OpenColorIO processor

            preset (dict): lut generic and sampling informations
        """
        pass

    @abstractmethod
    def get_default_preset(self):
        """ Return default preset
            See utils.lut_presets module
        """
        pass

    @staticmethod
    def get_export_message(file_path):
        """ Get export message

        Returns:
            .str

        """
        return "a new LUT was written in {1}".format(
                                                get_file_shortname(file_path),
                                                file_path)

    @staticmethod
    def is_int(test_range):
        """ Check if a range is int

        Args:
            test_range ([int/float, int/float]): range to test

        Returns:
            .boolean

        """
        is_int = False
        if (isinstance(test_range[0], int)
            and isinstance(test_range[1], int)):
            is_int = True
        return is_int

    @staticmethod
    def is_intput_int(preset):
        """ Check if a in range is int
        Returns:
            .boolean

        """
        return AbstractLUTHelper.is_int(preset[presets.IN_RANGE])

    @staticmethod
    def is_output_int(preset):
        """ Check if a out range is int
        Returns:
            .boolean

        """
        return AbstractLUTHelper.is_int(preset[presets.OUT_RANGE])

    @staticmethod
    def get_generated_title(file_path, preset):
        """ Title with file short name and ranges

        """
        return "{0} {1} {2}".format(get_file_shortname(file_path),
                                    preset[presets.IN_RANGE],
                                    preset[presets.OUT_RANGE])
