
#include "task2core.h"
#include <queue>
#include <vector>
#include "math.h"
#include "log.h"

enum core_prio_t { BEEFY, WIMPY };

g_vector<bool> Task2CoreScheduler::computeAffinity(
    uint32_t numCores, uint32_t parallelism, uint32_t workload, uint32_t sharing
) {
    //Map process properties to a 0.0 - 1.0 scale
    float parrelism_f = static_cast<float>(parallelism) / 100.0;
    float workload_f = static_cast<float>(workload) / 100.0;
    float sharing_f = static_cast<float>(sharing) / 100.0;

    //Map to intermediate parameters
    float core_size = _compute_core_size(parrelism_f, workload_f, sharing_f);
    float diversity = _compute_diversity(parrelism_f, workload_f, sharing_f);

    //Define queues of core for the scheduler to choose from
    //The scheduler will pick from these queues until the size and
    //diversity criteria are met
    std::queue<size_t> beefy_cores; beefy_cores.push(0); beefy_cores.push(1);
    std::queue<size_t> wimpy_cores; wimpy_cores.push(2); wimpy_cores.push(3);

    //The size priority determines which core we choose from first
    core_prio_t prio = (core_size > 0.5) ? BEEFY : WIMPY;
    //The number of cores determines when to stop choosing cores
    size_t cores = static_cast<size_t>(ceil(diversity * numCores));

    //Core allocator
    std::vector<size_t> scheduled_cores;
    for (size_t i = 0; i < cores; i++) {
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
    g_vector<bool> mask(numCores, false);
    for (size_t i = 0; i < scheduled_cores.size(); i++) {
        mask[scheduled_cores[i]] = true;
    }
    return mask;
}

float Task2CoreScheduler::_compute_core_size(float parallelism, float workload, float sharing)
{
    static const float PARALLELISM_CONTRIBUTION = 0.25;
    static const float WORKLOAD_CONTRIBUTION    = 0.50;
    static const float SHARING_CONTRIBUTION     = 0.25;

    return  (PARALLELISM_CONTRIBUTION * (1.0 - parallelism)) +
            (WORKLOAD_CONTRIBUTION * workload) +
            (SHARING_CONTRIBUTION * (1.0 - sharing));
}

float Task2CoreScheduler::_compute_diversity(float parallelism, float workload, float sharing)
{
    static const float PARALLELISM_CONTRIBUTION = 0.50;
    static const float WORKLOAD_CONTRIBUTION    = 0.00;
    static const float SHARING_CONTRIBUTION     = 0.50;

    return  (PARALLELISM_CONTRIBUTION * parallelism) +
            (WORKLOAD_CONTRIBUTION * workload) +
            (SHARING_CONTRIBUTION * sharing);
}
