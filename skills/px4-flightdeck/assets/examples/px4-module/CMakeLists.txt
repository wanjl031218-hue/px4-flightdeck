# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 PX4 Development Team. All rights reserved.
# Adapted for PX4 FlightDeck; see LICENSE.
px4_add_module(
    MODULE examples__flightdeck_observer
    MAIN flightdeck_observer
    SRCS FlightDeckObserver.cpp
    DEPENDS px4_work_queue
)
