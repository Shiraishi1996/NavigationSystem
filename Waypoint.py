#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Waypoint.py
#
# Solar-boat Project 2019
#   created on: 2019/07/27
#   Author: Tetsuro Ninomiya
#


class Waypoint:
    def __init__(self, latitude=None, longitude=None):
        if longitude is None:
            longitude = []
        if latitude is None:
            latitude = []
        self.latitude = latitude
        self.longitude = longitude
        self.__index = 0
        self.__num = 0

    def add_point(self, latitude, longitude):
        self.latitude.append(latitude)
        self.longitude.append(longitude)
        self.__num += 1
        return

    def get_point(self):
        latitude = self.latitude[self.__index]
        longitude = self.longitude[self.__index]
        return [latitude, longitude]

    def next_point(self):
        self.__index += 1
        if self.__index == self.__num:
            return False
        else:
            return True


if __name__ == "__main__":
    print("waypoint")
