""" Colorspace definitions

.. moduleauthor:: `Marie FETIVEAU <github.com/mfe>`_

"""
from abc import ABCMeta, abstractmethod
import math


class AbstractColorspace:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_red_primaries(self):
        """Return colorspace primaries

        Returns:
            .float, float

        """
        pass

    @abstractmethod
    def get_green_primaries(self):
        """Return colorspace primaries

        Returns:
            .float, float

        """
        pass

    @abstractmethod
    def get_blue_primaries(self):
        """Return colorspace primaries

        Returns:
            .float, float

        """
        pass

    @abstractmethod
    def get_white_point(self):
        """Return white coords

        Returns:
            .numpy.matrix (3x1)

        """
        pass

    @abstractmethod
    def lin_to_gamma(self, value):
        """Convert value from lin to gamma

        Args:
            value (float): value to transform

        Returns:
            .float

        """
        pass

    @abstractmethod
    def gamma_to_lin(self, value):
        """Convert value from lin to gamma

        Args:
            value (float): value to transform

        Returns:
            .float

        """
        pass


class Rec709(AbstractColorspace):
    """rec709 colorspace

    """
    def get_red_primaries(self):
        return 0.64, 0.33

    def get_green_primaries(self):
        return 0.30, 0.60

    def get_blue_primaries(self):
        return 0.15, 0.06

    def get_white_point(self):
        return 0.3127, 0.3290

    def lin_to_gamma(self, value):
        if value < 0.018:
            value *= 4.5
        else:
            value = float(pow(value, 0.45)*1.099 - 0.099)
        return value

    def gamma_to_lin(self, value):
        if value < 0.081:
            value *= 1.0/4.5
        else:
            value = float(pow((value + 0.099) * (1.0/1.099), 1.0/0.45))
        return value


class AlexaLogCV3(AbstractColorspace):
    """AlexaLogCV3 colorspace

    """
    def get_red_primaries(self):
        return 0.6840, 0.3130

    def get_green_primaries(self):
        return 0.2210, 0.8480

    def get_blue_primaries(self):
        return 0.0861, -0.1020

    def get_white_point(self):
        return 0.3127, 0.3290

    def lin_to_gamma(self, value):
        if value > 0.010591:
            value = (0.247190 * math.log10(5.555556 * value + 0.052272)
                     + 0.385537)
        else:
            value = 5.367655 * value + 0.092809
        return value

    def gamma_to_lin(self, value):
        if value > 0.1496582:
            value = (math.pow(10.0, (value - 0.385537) / 0.2471896) * 0.18
                     - 0.00937677)
        else:
            value = (value / 0.9661776 - 0.04378604) * 0.18 - 0.00937677
        return value

REC709 = Rec709()
ALEXALOGCV3 = AlexaLogCV3()