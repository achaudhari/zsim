#ifndef TASK2CORE_H_
#define TASK2CORE_H_

#include <stdint.h>
#include "g_std/g_vector.h"

class Task2CoreScheduler {
public:
static g_vector<bool> computeAffinity(
    uint32_t numCores, uint32_t parallelism, uint32_t workload, uint32_t sharing);

};

#endif  // TASK2CORE_H_
