#include "pseudo_lru.h"

#include <algorithm>
#include <cassert>

pseudo_lru::pseudo_lru(CACHE* cache) : pseudo_lru(cache, cache->NUM_SET, cache->NUM_WAY) {}

pseudo_lru::pseudo_lru(CACHE* cache, long sets, long ways) : replacement(cache), ways_trees(sets, pseudo_lru_ways_tree(ways)) {}

long pseudo_lru::find_victim(uint32_t triggering_cpu, uint64_t instr_id, long set, const champsim::cache_block* current_set, champsim::address ip,
                             champsim::address full_addr, access_type type)
{
  return ways_trees.at(static_cast<std::size_t>(set)).victim();
}

void pseudo_lru::replacement_cache_fill(uint32_t triggering_cpu, long set, long way, champsim::address full_addr, champsim::address ip,
                                        champsim::address victim_addr, access_type type)
{
  ways_trees.at(static_cast<std::size_t>(set)).update(way);
}

void pseudo_lru::update_replacement_state(uint32_t triggering_cpu, long set, long way, champsim::address full_addr, champsim::address ip,
                                          champsim::address victim_addr, access_type type, uint8_t hit)
{
  if (hit && type != access_type::WRITE) // Skip this for writeback hits
    ways_trees.at(static_cast<std::size_t>(set)).update(way);
}


pseudo_lru_ways_tree::pseudo_lru_ways_tree(long ways)
{
  std::size_t level_nodes = 1;
  while (ways > 1) {
    levels.emplace_back(level_nodes, pointer_direction::LEFT);
    ways /= 2;
    level_nodes *= 2;
  }
}

long pseudo_lru_ways_tree::victim()
{
  long level_idx = 0;
  for (auto it = levels.begin(); it != levels.end(); ++it) {
    const auto& level = *it;
    const auto& node = level[level_idx];
    if (node == pointer_direction::LEFT) {
      level_idx = 2 * level_idx;
    }
    else {
      level_idx = 2 * level_idx + 1;
    }
  }
  return level_idx;
}

void pseudo_lru_ways_tree::update(long way)
{
  long level_idx = way / 2;
  for (auto it = levels.rbegin(); it != levels.rend(); ++it) {
    auto& level = *it;
    auto& node = level[level_idx];
    if (node == pointer_direction::LEFT) {
      node = pointer_direction::RIGHT;
    }
    else {
      node = pointer_direction::LEFT;
    }
    level_idx /= 2;
  }
}
