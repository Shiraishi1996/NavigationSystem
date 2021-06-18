#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Status.py
#
# Solar-boat Project 2019
#   created on: 2019/07/27
#   Author: Tetsuro Ninomiya
#

import math

from GpsData import GpsData
from Params import Params
from Waypoint import Waypoint


class Status:
    def __init__(self, params):
        self.params = params
        self.waypoint = Waypoint()
        self.mode = "TEST"
        self.speed = 0.0
        self.boat_direction = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.timestamp_string = ""
        self.target_direction = 0.0
        self.target_distance = 0.0
        self.gps_data = GpsData()
        self.gps_data_for_out_of_range = None

    def read_gps(self):
        if self.gps_data.read():
            diff = abs(self.longitude - self.gps_data.longitude) + abs(
                self.latitude - self.gps_data.latitude
            )
            if diff >= 0.000001:
                self.boat_direction = self._get_direction(
                    self.longitude,
                    self.latitude,
                    self.gps_data.longitude,
                    self.gps_data.latitude,
                )
            self.timestamp_string = self.gps_data.timestamp_string
            if not self.gps_data_for_out_of_range:
                self.gps_data_for_out_of_range = {
                    "latitude": self.gps_data.latitude,
                    "longitude": self.gps_data.longitude,
                }
            self.latitude = self.gps_data.latitude
            self.longitude = self.gps_data.longitude
            self.speed = self.gps_data.speed[2]  # kph
            return True
        else:
            return False

    def calc_target_distance(self):
        r = 6378.137  # [km] # radius of the Earth
        wp = self.waypoint
        lon1 = math.radians(self.longitude)
        lat2, lon2 = map(math.radians, wp.get_point())
        lat1 = math.radians(self.latitude)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        self.target_distance = c * r * 1000  # [m]
        return

    def calc_target_direction(self):
        wp = self.waypoint
        rad_lon_a = math.radians(self.longitude)
        rad_lat_b, rad_lon_b = map(math.radians, wp.get_point())
        rad_lat_a = math.radians(self.latitude)
        d_long = rad_lon_b - rad_lon_a
        y = math.sin(d_long) * math.cos(rad_lat_b)
        x = math.cos(rad_lat_a) * math.sin(rad_lat_b) - math.sin(rad_lat_a) * math.cos(
            rad_lat_b
        ) * math.cos(d_long)
        dir = math.degrees(math.atan2(y, x)) % 360
        self.target_direction = dir  # degrees
        return

    @staticmethod
    def _get_direction(lon_a, lat_a, lon_b, lat_b):
        rad_lon_a = math.radians(lon_a)
        rad_lat_a = math.radians(lat_a)
        rad_lon_b = math.radians(lon_b)
        rad_lat_b = math.radians(lat_b)
        d_long = rad_lon_b - rad_lon_a
        y = math.sin(d_long) * math.cos(rad_lat_b)
        x = math.cos(rad_lat_a) * math.sin(rad_lat_b) - math.sin(rad_lat_a) * math.cos(
            rad_lat_b
        ) * math.cos(d_long)
        dir = math.degrees(math.atan2(y, x)) % 360
        return dir

    def _has_passed_way_point(self):
        return self.target_distance < 90.0

    def update_target(self):
        if self._has_passed_way_point():
            # If the boat has passed all waypoints, key is false
            # If not, key is true
            key = self.waypoint.next_point()
            if not key:
                print("AN has finished!")
                self.mode = "RC"
        return

    def update_way_point(self):
        try:
            self.waypoint = Waypoint(
                [self.gps_data_for_out_of_range["latitude"]],
                [self.gps_data_for_out_of_range["longitude"]],
            )
        except TypeError:
            print("Error: No gps_data_history but now out of range!")


if __name__ == "__main__":
    params = Params()
    status = Status(params)
