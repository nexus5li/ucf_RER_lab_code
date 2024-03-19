from time import sleep, time

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set

class Lakeshore325(Instrument):
    
    def __init__(self, adapter, **kwargs):
        super().__init__(
            adapter,
            "Lake Shore 32 Temperature Controller",
            **kwargs
        )
    
    temperature_A = Instrument.measurement(
        "KRDG? A",
        """ Reads the temperature of the sensor A in Kelvin. """
    )
    
    temperature_B = Instrument.measurement(
        "KRDG? B",
        """ Reads the temperature of the sensor B in Kelvin. """
    )

    setpoint_1 = Instrument.control(
        "SETP? 1", "SETP 1, %g",
        """ A floating point property that controls the setpoint temperature
        in Kelvin for Loop 1. """
    )
    setpoint_2 = Instrument.control(
        "SETP? 2", "SETP 2, %g",
        """ A floating point property that controls the setpoint temperature
        in Kelvin for Loop 2. """
    )
    
    heater_range = Instrument.control(
        "RANGE?", "RANGE 1, %d",
        """ A string property that controls the heater range, which
        can take the values: off, low, medium, and high. These values
        correlate to 0, 0.5, 5 and 50 W respectively. """,
        validator=strict_discrete_set,
        values={'off': 0, 'low': 1, 'high': 2},
        map_values=True
    )
    
    
    def disable_heater(self):
        """ Turns the :attr:`~.heater_range` to :code:`off` to disable the heater. """
        self.heater_range = 'off'
        
    def wait_for_temperature(self, accuracy=0.3,
                             interval=0.1, sensor='A', setpoint=1, timeout=360,
                             should_stop=lambda: False, sleep_time = 60):
        """ Blocks the program, waiting for the temperature to reach the setpoint
        within the accuracy (%), checking this each interval time in seconds.
        :param accuracy: An acceptable percentage deviation between the
                         setpoint and temperature
        :param interval: A time in seconds that controls the refresh rate
        :param sensor: The desired sensor to read, either A or B
        :param setpoint: The desired setpoint loop to read, either 1 or 2
        :param timeout: A timeout in seconds after which an exception is raised
        :param should_stop: A function that returns True if waiting should stop, by
                            default this always returns False
        """
        temperature_name = 'temperature_%s' % sensor
        setpoint_name = 'setpoint_%d' % setpoint
        # Only get the setpoint once, assuming it does not change
        setpoint_value = getattr(self, setpoint_name)

        def percent_difference(temperature):
            return abs(100 * (temperature - setpoint_value) / setpoint_value)
        t = time()
        while percent_difference(getattr(self, temperature_name)) > accuracy:
            sleep(interval)
            if (time() - t) > timeout:
                raise Exception((
                    "Timeout occurred after waiting %g seconds for "
                    "the LakeShore 325 temperature to reach %g K."
                ) % (timeout, setpoint))
            if should_stop():
                return
        print(f'In wait_for_tem()Reached temperature preset: {setpoint_value}, actual value: {getattr(self, temperature_name)}')
        sleep(sleep_time)
        print(f"Having slept for {sleep_time} seconds in wait_for_temp() method")