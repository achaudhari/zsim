
#include "task2core.h"
#include <queue>
#include <vector>
#include "math.h"
#include "log.h"

static const bool USE_REGRESSION_BASED_SCHEDULER = false;

enum core_prio_t { BEEFY, WIMPY };

g_vector<bool> Task2CoreScheduler::computeAffinity(
    uint32_t total_num_cores, uint32_t energy, uint32_t phase,
    uint32_t l1misses, uint32_t l2misses, uint32_t sharing
) {
    static const size_t MAX_CORES_PER_TASK = 4;

    //Map process properties to a 0.0 - 1.0 scale
    //Normalize to max values
    float energy_f = static_cast<float>(energy) / 108.0;
    float phase_f = static_cast<float>(phase) / 1.0;
    float l1misses_f = static_cast<float>(l1misses) / 2515517.0;
    float l2misses_f = static_cast<float>(l2misses) / 661065.0;
    float sharing_f = static_cast<float>(sharing) / 1007.0;

    //Map to intermediate parameters
    float core_size = _compute_core_size(energy_f, phase_f, l1misses_f, l2misses_f, sharing_f);
    float allowance = _compute_allowance(energy_f, phase_f, l1misses_f, l2misses_f, sharing_f);

    //Define queues of core for the scheduler to choose from
    //The scheduler will pick from these queues until the size and
    //allowance criteria are met
    std::queue<size_t> beefy_cores; beefy_cores.push(0); beefy_cores.push(1);
    std::queue<size_t> wimpy_cores; wimpy_cores.push(2); wimpy_cores.push(3);

    //The size priority determines which core we choose from first
    core_prio_t prio = (core_size > 0.5) ? BEEFY : WIMPY;
    //The number of cores determines when to stop choosing cores
    size_t num_cores = static_cast<size_t>(ceil(allowance * MAX_CORES_PER_TASK));

    //Core allocator
    std::vector<size_t> scheduled_cores;
    for (size_t i = 0; i < num_cores; i++) {
        std::queue<size_t>& preferred_queue = (prio==BEEFY) ? beefy_cores : wimpy_cores;
        std::queue<size_t>& other_queue     = (prio==BEEFY) ? wimpy_cores : beefy_cores;
        if (!preferred_queue.empty()) {
            scheduled_cores.push_back(preferred_queue.front());
            preferred_queue.pop();
        } else if (!other_queue.empty()) {
            scheduled_cores.push_back(other_queue.front());
            other_queue.pop();
        } else {
            //No-op. No cores left to schedule.
        }
    }

    //Translate core allocation to mask
    g_vector<bool> mask(total_num_cores, false);
    for (size_t i = 0; i < scheduled_cores.size(); i++) {
        mask[scheduled_cores[i]] = true;
    }
    return mask;
}

float Task2CoreScheduler::_compute_core_size(
    float energy, float phase, float l1misses_f, float l2misses_f, float sharing)
{
    if (USE_REGRESSION_BASED_SCHEDULER) {
        //TODO: Implement scheduler
        return 1.0;
    } else {
        return (((1.0 - energy) * 0.5) +
                (phase * 0.0) +
                (l1misses_f * 0.2) +
                (l2misses_f * 0.3) +
                (sharing * 0.0));
    }
}

float Task2CoreScheduler::_compute_allowance(
    float energy, float phase, float l1misses_f, float l2misses_f, float sharing)
{
    if (USE_REGRESSION_BASED_SCHEDULER) {
        //TODO: Implement scheduler
        return 1.0;
    } else {
        return (((1.0 - energy) * 0.4) +
                (phase * 0.0) +
                (l1misses_f * 0.2) +
                (l2misses_f * 0.0) +
                (sharing * 0.4));
    }
}
