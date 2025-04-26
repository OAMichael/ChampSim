#include "markov_probability.h"

#include <random>

bool markov_probability::predict_branch(champsim::address ip)
{
  auto counter = frequency_counters[hash(ip)];

  double taken_prob = 0.5f;
  std::size_t sum = counter.taken + counter.not_taken;
  if (sum != 0) {
    taken_prob = static_cast<double>(counter.taken) / static_cast<double>(sum);
  }

  static std::random_device rd;
  static std::mt19937 mt(rd());
  static std::uniform_real_distribution<> dist(0.0, 1.0);

  return dist(mt) <= taken_prob;
}

void markov_probability::last_branch_result(champsim::address ip, champsim::address branch_target, bool taken, uint8_t branch_type)
{
  auto& counter = frequency_counters[hash(ip)];
  if (taken) {
    ++counter.taken;
  }
  else {
    ++counter.not_taken;
  }
}
