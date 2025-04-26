#ifndef BRANCH_MARKOV_PROBABILITY_H
#define BRANCH_MARKOV_PROBABILITY_H

#include <array>

#include "address.h"
#include "modules.h"

class markov_probability : champsim::modules::branch_predictor
{
  [[nodiscard]] static constexpr auto hash(champsim::address ip) { return ip.to<unsigned long>() % PRIME; }

  static constexpr std::size_t TABLE_SIZE = 16384;
  static constexpr std::size_t PRIME = 16381;

  struct frequency_counter {
    std::size_t taken = 0;
    std::size_t not_taken = 0;
  };

  std::array<frequency_counter, TABLE_SIZE> frequency_counters;

public:
  using branch_predictor::branch_predictor;

  // void initialize_branch_predictor();
  bool predict_branch(champsim::address ip);
  void last_branch_result(champsim::address ip, champsim::address branch_target, bool taken, uint8_t branch_type);
};

#endif
