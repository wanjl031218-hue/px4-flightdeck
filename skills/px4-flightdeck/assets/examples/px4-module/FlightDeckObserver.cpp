// SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2021 PX4 Development Team. All rights reserved.
// Copyright (c) 2026 PX4 FlightDeck contributors.
// Lifecycle adapted from PX4 src/examples/work_item; see LICENSE.

#include <px4_platform_common/module.h>
#include <px4_platform_common/log.h>
#include <px4_platform_common/px4_work_queue/ScheduledWorkItem.hpp>
#include <uORB/Subscription.hpp>
#include <uORB/topics/vehicle_local_position.h>
#include <drivers/drv_hrt.h>

class FlightDeckObserver final : public ModuleBase<FlightDeckObserver>, public px4::ScheduledWorkItem
{
public:
    FlightDeckObserver() : ScheduledWorkItem(MODULE_NAME, px4::wq_configurations::test1) {}
    ~FlightDeckObserver() override { ScheduleClear(); }

    static int task_spawn(int argc, char *argv[])
    {
        auto *instance = new FlightDeckObserver();
        if (!instance) { return PX4_ERROR; }
        _object.store(instance);
        _task_id = task_id_is_work_queue;
        instance->ScheduleOnInterval(1000000); // 1 Hz; services stop even without samples.
        return PX4_OK;
    }

    static int custom_command(int argc, char *argv[]) { return print_usage("unknown command"); }
    static int print_usage(const char *reason = nullptr)
    {
        if (reason) { PX4_WARN("%s", reason); }
        PRINT_MODULE_DESCRIPTION("Read-only local NED position observer; no commands or writes.");
        PRINT_MODULE_USAGE_NAME("flightdeck_observer", "template");
        PRINT_MODULE_USAGE_COMMAND("start");
        PRINT_MODULE_USAGE_DEFAULT_COMMANDS();
        return 0;
    }
    int print_status() override
    {
        PX4_INFO("running: read-only 1 Hz local-position subscription");
        return 0;
    }

private:
    void Run() override
    {
        if (should_exit()) {
            ScheduleClear();
            exit_and_cleanup();
            return;
        }
        vehicle_local_position_s position{};
        if (_position.update(&position)) {
            const auto now = hrt_absolute_time();
            if (position.timestamp == 0 || position.timestamp > now) {
                PX4_WARN("invalid/future PX4 timestamp");
                return;
            }
            PX4_INFO("NED=(%.3f, %.3f, %.3f) valid_xy=%d valid_z=%d age_ms=%.1f reset_xy=%u reset_z=%u",
                     (double)position.x, (double)position.y, (double)position.z,
                     (int)position.xy_valid, (int)position.z_valid,
                     (double)(now - position.timestamp) / 1000.0,
                     (unsigned)position.xy_reset_counter, (unsigned)position.z_reset_counter);
        } else {
            PX4_INFO("no new local-position sample");
        }
    }
    uORB::Subscription _position{ORB_ID(vehicle_local_position)};
};

extern "C" __EXPORT int flightdeck_observer_main(int argc, char *argv[])
{
    return FlightDeckObserver::main(argc, argv);
}
