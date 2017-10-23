import logging
import time

from _thread import start_new_thread
from math import ceil, floor


class Acc():
    DISTANCE_CAP_METRES = 3
    DISTANCE_CAP_CENTIMETRES = DISTANCE_CAP_METRES * 100
    SAFE_DISTANCE = 40
    WANTED_DISTANCE = 50
    DIST_DATA_LIFETIME = 1

    def __init__(self, core):
        self.distance_list = []
        self.distance_time_list = []
        self.core = core
        self.speed = 0
        self.wanted_speed = 0
        self.current_speed = 0

        self.debug_string = ""

        start_new_thread(self.__acc_on, ())

    def __acc_on(self):
        logging.info("Started acc_on")

        last_time = time.time()

        while True:

            d_distance = self.__get_distance()

            # If we have no value, set speed to 0 as a safety measure

            d_velocity = self.__get_delta_v_for_forward_object()

            curr_time = int(time.time())
            if curr_time % 3 == 0 and curr_time != last_time:
                logging.info("{} : {} suggest speed : {} | d_dist : {} | d_velo : {} | dbg : {}".format(
                    curr_time,
                    type(self).__name__,
                    self.speed,
                    d_distance,
                    d_velocity,
                    self.debug_string
                ))
                last_time = curr_time

            if d_distance is None or d_velocity is None:
                self.speed = 0
                continue

            if d_distance >= self.DISTANCE_CAP_CENTIMETRES:
                self.debug_string = "NO DETECTED TARGET"
                # in case of no obstacles, go for desired speed
                if self.current_speed != self.wanted_speed:
                    self.speed = self.wanted_speed
            elif d_distance < self.SAFE_DISTANCE:  # decrease speed if too close to target
                self.debug_string = "TOO CLOSE TO TARGET"
                self.__set_speed(-self.wanted_speed)
            elif d_distance > self.WANTED_DISTANCE:  # increase speed if too far away from target
                self.debug_string = "NOT CLOSE ENOUGH TO TARGET"
                self.__set_speed(self.wanted_speed)
            elif d_velocity < 0:  # decrease speed if moving too fast relative to target
                self.debug_string = "TOO FAST"
                self.__change_speed(d_velocity)
            elif d_velocity > 0:  # increase speed if too slow relative to target
                self.debug_string = "GOTTA GO FAST"
                self.__change_speed(d_velocity)
            else:
                self.debug_string = "NOTHING HAPPENS"

    def __change_speed(self, delta_v):
        delta_v = float(delta_v)
        self.__set_speed(delta_v + self.current_speed)

    def __set_speed(self, speed):
        # Should prevent MOPED from backing when "braking" at current speed = 0
        if self.current_speed is 0 and speed < 0:
            self.speed = 0
        else:
            if abs(speed) > self.wanted_speed:
                if speed < 0:
                    self.speed = -self.wanted_speed
                else:
                    self.speed = self.wanted_speed
            else:
                self.speed = speed

    # Gets distance to preceding vehicle, if not more than 2
    def __get_distance(self):
        if len(self.core.get_ultra_data()) == 0:
            return None

        try:
            (timestamp, dist) = self.core.get_ultra_data()[0]
        except IndexError:
            return None  # None values are handled in the loop

        if len(self.distance_time_list) is 0:
            self.__update_lists(timestamp, dist)
        elif timestamp != self.distance_time_list[-1]:
            self.__update_lists(timestamp, dist)

        return self.__get_average_of(self.distance_list)

    def __update_lists(self, timestamp, dist):
        self.distance_list.append(min(dist, self.DISTANCE_CAP_CENTIMETRES))
        self.distance_time_list.append(timestamp)

        self.__check_timestamp_validity()

    # Remove too old data (threshold = DIST_DATA_LIFETIME)
    def __check_timestamp_validity(self):
        while time.clock() - self.distance_time_list[0] > self.DIST_DATA_LIFETIME:
            self.distance_list = self.distance_list[1:]
            self.distance_time_list = self.distance_time_list[1:]

    # Approximates the difference in speed to
    # the target by using constructing a
    # linear function from two (distance, time) points
    def __get_delta_v_for_forward_object(self):
        size = len(self.distance_list)
        if not size:
            return

        # values to determine the size of the slices from the data list
        half_point_ceiled = ceil(size / 2)
        half_point_floored = floor(size / 2)
        if half_point_ceiled == half_point_floored:
            half_point_floored -= 1

        # The point p0
        d0 = self.__get_average_of(self.distance_list[half_point_ceiled:])
        t0 = self.__get_average_of(self.distance_time_list[half_point_ceiled:])

        # The point p1
        d1 = self.__get_average_of(self.distance_list[:half_point_floored])
        t1 = self.__get_average_of(self.distance_time_list[:half_point_floored])

        # The incline between p0 and p1 is the relative speed
        d_distance = d1 - d0
        d_time = t1 - t0

        if d_distance is 0 or d_time is 0:
            return None

        return d_distance / d_time

    @staticmethod
    def __get_average_of(my_list):
        if not len(my_list):
            return 0  # see no evil

        avg = 0
        for val in my_list:
            avg = avg + val
        avg = avg / len(my_list)
        return avg
