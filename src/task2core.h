#ifndef TASK2CORE_H_
#define TASK2CORE_H_

#include <stdint.h>
#include "g_std/g_vector.h"

class Task2CoreScheduler {
public:
    static g_vector<bool> computeAffinity(
        uint32_t numCores, uint32_t energy, uint32_t phase,
        uint32_t l1misses, uint32_t l2misses, uint32_t sharing);

private:
    enum core_prio_t { BEEFY, WIMPY };

    static size_t _beefy_core_idx;
    static size_t _wimpy_core_idx;

    static size_t _get_next_core(core_prio_t prio);

    static float _compute_core_size(
        float energy, float phase, float l1misses_f, float l2misses_f, float sharing);

    static float _compute_allowance(
        float energy, float phase, float l1misses_f, float l2misses_f, float sharing);
};

#endif  // TASK2CORE_H_
