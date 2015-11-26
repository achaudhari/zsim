
#include "task2core.h"
#include <queue>
#include <vector>
#include "math.h"
#include "log.h"

static const bool USE_REGRESSION_BASED_SCHEDULER = false;

size_t Task2CoreScheduler::_beefy_core_idx = 0;
size_t Task2CoreScheduler::_wimpy_core_idx = 0;

g_vector<bool> Task2CoreScheduler::computeAffinity(
    uint32_t total_num_cores, uint32_t energy, uint32_t phase,
    uint32_t l1misses, uint32_t l2misses, uint32_t sharing
) {
    static const size_t MAX_CORES_PER_TASK = 4;

    //Map process properties to a 0.0 - 1.0 scale
    //Normalize to max values
    float energy_f = static_cast<float>(energy) / 108.0;
    float phase_f = static_cast<float>(phase) / 12784.0;
    float l1misses_f = static_cast<float>(l1misses) / 2515517.0;
    float l2misses_f = static_cast<float>(l2misses) / 661065.0;
    float sharing_f = static_cast<float>(sharing) / 1007.0;

    dbg("          * Params = {energy:%f, phase:%f, l1misses:%f, l2misses:%f, sharing:%f}",
        energy_f, phase_f, l1misses_f, l2misses_f, sharing_f);

    //Map to intermediate parameters
    float core_size = _compute_core_size(energy_f, phase_f, l1misses_f, l2misses_f, sharing_f);
    float allowance = _compute_allowance(energy_f, phase_f, l1misses_f, l2misses_f, sharing_f);

    //The size priority determines which core we choose from first
    core_prio_t pref_core = (core_size > 0.5) ? BEEFY : WIMPY;
    core_prio_t alt_core = (core_size > 0.5) ? WIMPY : BEEFY;
    //The number of cores determines when to stop choosing cores
    size_t num_cores = static_cast<size_t>(ceil(allowance * MAX_CORES_PER_TASK));
    size_t pref_cores_left = 2;

    dbg("          * Intermediates = {core_size:%s, allowance:%d}",
        (pref_core==BEEFY?"BEEFY":"WIMPY"), int(num_cores));

    //Core allocator
    //First choose from preferred pool then dip into the alternate pool
    std::vector<size_t> scheduled_cores;
    for (size_t i = 0; i < num_cores; i++) {
        if (pref_cores_left > 0) {
            scheduled_cores.push_back(_get_next_core(pref_core));
            pref_cores_left--;
        } else {
            scheduled_cores.push_back(_get_next_core(alt_core));
        }
    }

    //Translate core allocation to mask
    g_vector<bool> mask(total_num_cores, false);
    for (size_t i = 0; i < scheduled_cores.size(); i++) {
        mask[scheduled_cores[i]] = true;
    }
    return mask;
}

size_t Task2CoreScheduler::_get_next_core(core_prio_t prio) {
    static const size_t BEEFY_CORES[2] = {0, 1};
    static const size_t WIMPY_CORES[2] = {2, 3};

    size_t core = 0;
    if (prio == BEEFY) {
        core = BEEFY_CORES[_beefy_core_idx];
        _beefy_core_idx = (_beefy_core_idx + 1) % 2;
    } else {
        core = WIMPY_CORES[_wimpy_core_idx];
        _wimpy_core_idx = (_wimpy_core_idx + 1) % 2;
    }
    return core;
}

float Task2CoreScheduler::_compute_core_size(
    float energy, float phase, float l1misses_f, float l2misses_f, float sharing)
{
    if (USE_REGRESSION_BASED_SCHEDULER) {
        //TODO: Implement scheduler
        return 1.0;
    } else {
        return (((1.0 - energy) * 0.3) +
                (phase * 0.3) +
                (l1misses_f * 0.2) +
                (l2misses_f * 0.2) +
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
        return (((1.0 - energy) * 0.2) +
                (phase * 0.4) +
                (l1misses_f * 0.0) +
                (l2misses_f * 0.0) +
                (sharing * 0.4));
    }
}
