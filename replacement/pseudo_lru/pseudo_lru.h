#ifndef REPLACEMENT_PSEUDO_LRU_H
#define REPLACEMENT_PSEUDO_LRU_H

#include <vector>

#include "cache.h"
#include "modules.h"

class pseudo_lru_ways_tree
{
  enum pointer_direction : uint8_t
  {
    LEFT,
    RIGHT,
    NUM_DIRECTIONS = 2
  };
  
  using ways_tree_node = pointer_direction;
  using ways_tree_level = std::vector<ways_tree_node>;

  std::vector<ways_tree_level> levels;

public:
  explicit pseudo_lru_ways_tree(long ways);

  long victim();
  void update(long way);
};


class pseudo_lru : public champsim::modules::replacement
{
  std::vector<pseudo_lru_ways_tree> ways_trees;

public:
  explicit pseudo_lru(CACHE* cache);
  pseudo_lru(CACHE* cache, long sets, long ways);

  // void initialize_replacement();
  long find_victim(uint32_t triggering_cpu, uint64_t instr_id, long set, const champsim::cache_block* current_set, champsim::address ip,
                   champsim::address full_addr, access_type type);
  void replacement_cache_fill(uint32_t triggering_cpu, long set, long way, champsim::address full_addr, champsim::address ip,
                              champsim::address victim_addr, access_type type);
  void update_replacement_state(uint32_t triggering_cpu, long set, long way, champsim::address full_addr, champsim::address ip,
                                champsim::address victim_addr, access_type type, uint8_t hit);
  // void replacement_final_stats()
};

#endif
