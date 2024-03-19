import logging
import weakref
import time
import re
import numpy as np
import pandas as pd
from enum import IntEnum
from collections import Counter, namedtuple, OrderedDict
from pymeasure.instruments.validators import (strict_discrete_set,
                                              strict_range,
                                              strict_discrete_range)

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

# Import Skeleton classes
from pymeasure.instruments import Instrument
from pymeasure.instruments.agilent import AgilentB1500
# Import Auxiliary classes
from pymeasure.instruments.agilent.agilentB1500 import SMU
from pymeasure.instruments.agilent.agilentB1500 import SMU
from pymeasure.instruments.agilent.agilentB1500 import SMUVoltageRanging
from pymeasure.instruments.agilent.agilentB1500 import SMUCurrentRanging
from pymeasure.instruments.agilent.agilentB1500 import Ranging
from pymeasure.instruments.agilent.agilentB1500 import MeasMode



class b1505a(AgilentB1500): # Overriden Skeleton B1505
    def __init__(self, connecterName, **kwargs):
        super().__init__(connecterName, **kwargs)
        """
            RER SMU setups:
            0:('GNDU','GNDU+ADC')
            1:('HPSMU','SMU1:HP')
            3:('HPSMU','SMU2:HP')
            5:('MFCMU','CMU1:MF')
            6:('HCSMU','SMU3:HC')
            8:('HVSMU','SMU4:HV')
        """
        # self._smu_names = {}
        # self._smu_references = {}
        self.GNDU = 11

    def query_modules(self):
        """ Queries module models from the instrument.
        Returns dictionary of channel and module type.

        :return: Channel:Module Type
        :rtype: dict
        """
        modules = self.ask('UNT?')
        modules = modules.split(';')
        module_names = {
            '0': 'GNDU+ADC', # GNDU
            'B1510A': 'HPSMU', # High Power SMU - SMU1
            'B1511B': 'MPSMU', # Medium Power SMU - SMU2
            'B1512A': 'HCSMU', # High Current SMU
            'B1513C': 'HCSMU', # High Voltage SMU
            'B1514A': 'MCSMU', # Medium Current SMU
            'B1520A': 'MFCMU', # Multi-ferquency SMU
        }
        out = {}
        for i, module in enumerate(modules):
            module = module.split(',')
            if not module[0] == '0':
                try:
                    out[i + 1] = module_names[module[0]]
                    # i+1: channels start at 1 not at 0
                except Exception:
                    raise NotImplementedError(
                        f'Module {module[0]} is not implented yet!')
        return out

    
    def meas_mode(self, mode, *args, channels=[]):
        """ Set Measurement mode of channels. Measurements will be taken in
        the same order as the SMU references are passed. (``MM``)

        :param mode: Measurement mode

            * Spot
            * Staircase Sweep
            * Sampling

        :type mode: :class:`.MeasMode`
        :param args: SMU references
        :type args: :class:`.SMU`
        """
        mode = MeasMode.get(mode)
        cmd = "MM %d" % mode.value
        print('arugment: ', args)
        if channels == []:
            for smu in args:
                if isinstance(smu, rerSMU):
                    cmd += ", %d" % smu.channel
        else:
            for smu in args:
                print('channel', smu.channel)
                if isinstance(smu, rerSMU) and smu.channel in channels:
                    cmd += ", %d" % smu.channel
                    print(f'excecuted: {cmd}')
        self.write(cmd)
        self.check_errors()


    def initialize_smu(self, channel, smu_type, name):
        """ Initializes SMU instance by calling :class:`.SMU`.

        :param channel: SMU channel
        :type channel: int
        :param smu_type: SMU type, e.g. ``'HRSMU'``
        :type smu_type: str
        :param name: SMU name for pymeasure (data output etc.)
        :type name: str
        :return: SMU instance
        :rtype: :class:`.SMU`
        """
        if channel in (
                list(range(101, 1101, 100))
                + list(range(102, 1102, 100))):
            channel = int(str(channel)[0:-2])
            # subchannels not relevant for SMU/CMU
        channel = strict_discrete_set(channel, range(1, 11))
        self._smu_names[channel] = name
        smu_reference = rerSMU(self, channel, smu_type, name)
        self._smu_references[channel] = smu_reference
        return smu_reference

    def read_channels_vxi(self):
        """ Reads data for 1 measurement point from the buffer. Specify number
        of measurement channels + sweep sources (depending on data
        output setting).

        :param nchannels: Number of channels which return data
        :type nchannels: int
        :return: Measurement data
        :rtype: tuple
        """
        # data = self.adapter.read(self._data_format.size * nchannels)
        data = self.adapter.read()
        print(data)
        # data = data.decode("ASCII")
        data = data.rstrip('\r,')
        # ',' if more data in buffer, '\r' if last data point
        data = data.split(',')
        data = map(self._data_format.format_single, data)
        data = tuple(data)
        return data

class rerSMU(SMU): # RER version of SMU class
    def __init__(self, parent, channel, smu_type, name, **kwargs):
        # to allow garbage collection for cyclic references
        self._b1500 = weakref.proxy(parent)
        channel = strict_discrete_set(channel, range(1, 11))
        self.channel = channel
        # smu_type = strict_discrete_set(  # No HRSMU in B1505
        #     smu_type,
        #     ['HRSMU', 'MPSMU', 'HPSMU', 'MCSMU', 'HCSMU',
        #         'DHCSMU', 'HVSMU', 'UHCU', 'HVMCU', 'UHVU'])

        smu_type = strict_discrete_set(smu_type,
            ['HPSMU', 'MPSMU', 'MCSMU', 'HCSMU',
                'HCSMU', 'HVSMU', 'UHCU', 'HVMCU', 'UHVU'])
        self.voltage_ranging = rerSMUVoltageRanging(smu_type)
        self.current_ranging = rerSMUCurrentRanging(smu_type)
        self.name = name

class rerSMUVoltageRanging(): # RER version of SMUVoltageRanging
    # Check pp335 for Allowable ranges
    def __init__(self, smu_type):
        supported_ranges = { 
            # 'HRSMU': [0, 5, 11, 20, 50, 12, 200, 13, 400, 14, 1000], # No HRSMU in 1505A
            'MPSMU': [0, 5, 11, 20, 50, 12, 200, 13, 400, 14, 1000],
            'HPSMU': [0, 11, 20, 12, 200, 13, 400, 14, 1000, 15, 2000], 
            'MCSMU': [0, 2, 11, 20, 12, 200, 13, 400], 
            'HCSMU': [0, 2, 11, 20, 12, 200, 13, 400],
            'DHCSMU': [0, 2, 11, 20, 12, 200, 13, 400],
            'HVSMU': [0, 15, 2000, 5000, 15000, 30000],
            'UHCU': [0, 14, 1000],
            'HVMCU': [0, 15000, 30000],
            'UHVU': [0, 103]
        }
        supported_ranges = supported_ranges[smu_type]

        ranges = {
            '0.2 V': 2,
            '0.5 V': 5,
            '2 V': (11, 20),
            '5 V': 50,
            '20 V': (12, 200),
            '40 V': (13, 400),
            '100 V': (14, 1000),
            '200 V': (15, 2000),
            '500 V': 5000,
            '1500 V': 15000,
            '3000 V': 30000,
            '10 kV': 103
        }

        # set range attributes
        self.output = Ranging(supported_ranges, ranges)
        self.meas = Ranging(supported_ranges, ranges,
                            fixed_ranges=True)

class rerSMUCurrentRanging(): # RER version of SMUCurrentRanging
    """ Provides Range Name/Index transformation for current
    measurement/sourcing.
    Validity of ranges is checked against the type of the SMU.

    Omitting the 'limited auto ranging'/'range fixed' specification in
    the range string for current measurement defaults to
    'limited auto ranging'.

    Full specification: '1 nA range fixed' or '1 nA limited auto ranging'

    '1 nA' defaults to '1 nA limited auto ranging'
    """
    # Check pp335 for Allowable ranges
    def __init__(self, smu_type):
        supported_output_ranges = {
            # in combination with ASU also 8
            # 'HRSMU': [0, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], # Again, we dont have HRSMU
            # in combination with ASU also 8,9,10
            'MPSMU': [0, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            'HPSMU': [0, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'MCSMU': [0, 15, 16, 17, 18, 19, 20],
            'HCSMU': [0, 15, 16, 17, 18, 19, 20, 22],
            'DHCSMU': [0, 15, 16, 17, 18, 19, 20, 21, 23],
            'HVSMU': [0, 11, 12, 13, 14, 15, 16, 17, 18],
            'UHCU': [0, 26, 28],
            'HVMCU': [],
            'UHVU': []
        }
        supported_meas_ranges = {
            **supported_output_ranges,
            # overwrite output ranges:
            'HVMCU': [0, 19, 21],
            'UHVU': [0, 15, 16, 17, 18, 19]
        }
        supported_output_ranges = supported_output_ranges[smu_type]
        supported_meas_ranges = supported_meas_ranges[smu_type]

        ranges = {
            '1 pA': 8,  # for ASU
            '10 pA': 9,
            '100 pA': 10,
            '1 nA': 11,
            '10 nA': 12,
            '100 nA': 13,
            '1 uA': 14,
            '10 uA': 15,
            '100 uA': 16,
            '1 mA': 17,
            '10 mA': 18,
            '100 mA': 19,
            '1 A': 20,
            '2 A': 21,
            '20 A': 22,
            '40 A': 23,
            '500 A': 26,
            '2000 A': 28
        }

        # set range attributes
        self.output = Ranging(supported_output_ranges, ranges)
        self.meas = Ranging(supported_meas_ranges, ranges,
                            fixed_ranges=True)