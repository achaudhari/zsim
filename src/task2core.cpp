
#include "task2core.h"

g_vector<bool> Task2CoreScheduler::computeAffinity(
    uint32_t numCores, uint32_t parallelism, uint32_t workload, uint32_t sharing
) {
    g_vector<bool> mask;
    mask.resize(numCores);

    //TODO: Implement me
    for (size_t i = 0; i < numCores; i++) {
        mask[i] = true;
    }

    return mask;
}
