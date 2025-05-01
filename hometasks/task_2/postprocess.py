import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


LRU_JSON_PATH        = '../replacement/lru/json/'
DRRIP_JSON_PATH      = '../replacement/drrip/json/'
PSEUDO_LRU_JSON_PATH = '../replacement/pseudo_lru/json/'
MRU_JSON_PATH        = '../replacement/mru/json/'
LFU_JSON_PATH        = '../replacement/lfu/json/'
PICTURES_PATH        = './pictures/'


class TraceStats:
    name: str
    miss_rate: float


def gmean(iterable):
    return np.exp(np.log(iterable).mean())


def parse_file_stats(filename):
    info = TraceStats()
    info.name = os.path.basename(filename)

    with open(filename) as f:
        all_stats = json.load(f)
        roi_stats = all_stats[0]['roi']['cpu0_L2C']

        access_stats = [
            roi_stats['LOAD'],
            roi_stats['PREFETCH'],
            roi_stats['RFO'],
            roi_stats['TRANSLATION'],
            roi_stats['WRITE']
        ]

        total_hits = 0
        total_misses = 0
        for stats in access_stats:
            for hit in stats['hit']:
                total_hits += int(hit)
            for miss in stats['miss']:
                total_misses += int(miss)

        info.miss_rate = total_misses / (total_misses + total_hits)

    return info


def parse_stats(dirname):
    traces_stats = []
    for filename in os.listdir(dirname):
        stats = parse_file_stats(dirname + filename)
        traces_stats.append(stats)
    return traces_stats


def plot_stats(lru_stats, drrip_stats, pseudo_lru_stats, mru_stats, lfu_stats):
    lru_miss_rate        = [stats.miss_rate for stats in lru_stats]
    drrip_miss_rate      = [stats.miss_rate for stats in drrip_stats]
    pseudo_lru_miss_rate = [stats.miss_rate for stats in pseudo_lru_stats]
    mru_miss_rate        = [stats.miss_rate for stats in mru_stats]
    lfu_miss_rate        = [stats.miss_rate for stats in lfu_stats]

    lru_miss_rate_gmean        = gmean(lru_miss_rate)
    drrip_miss_rate_gmean      = gmean(drrip_miss_rate)
    pseudo_lru_miss_rate_gmean = gmean(pseudo_lru_miss_rate)
    mru_miss_rate_gmean        = gmean(mru_miss_rate)
    lfu_miss_rate_gmean        = gmean(lfu_miss_rate)

    replacement_names = [
        "LRU",
        "DRRIP",
        "Pseudo-LRU",
        "MRU",
        "LFU"
    ]

    replacement_miss_rate_gmean = [
        lru_miss_rate_gmean,
        drrip_miss_rate_gmean, 
        pseudo_lru_miss_rate_gmean,
        mru_miss_rate_gmean,
        lfu_miss_rate_gmean
    ]

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    fig.suptitle('Replacement Policies Miss Rate', fontsize=20)
    ax.grid(zorder=0)
    ax.set_xlabel('Replacement Policy', fontsize=18)
    ax.set_ylabel('Miss Rate', fontsize=18)
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.tick_params(axis='both', which='major', labelsize=14)
    rects = ax.bar(replacement_names, replacement_miss_rate_gmean, align='center', zorder=2)
    ax.bar_label(rects, labels=[f"{100 * ms: .3f}%" for ms in replacement_miss_rate_gmean], padding=2, fontsize=16)
    fig.tight_layout()
    plt.savefig(PICTURES_PATH + 'miss_rate_gmean.pdf')
    plt.close()


    traces_names = [stats.name.split('.')[0] for stats in lru_stats]
    traces_count = len(traces_names)
    x = np.arange(traces_count)
    width = 0.1

    fig, ax = plt.subplots(1, 1, figsize=(24, 8))
    fig.suptitle('Replacement Policies Miss Rate', fontsize=20)
    ax.grid(zorder=0)
    ax.bar(x - 2 * width, lru_miss_rate,        width, color='tomato',     zorder=2, label='LRU')
    ax.bar(x - width,     drrip_miss_rate,      width, color='dodgerblue', zorder=2, label='DRRIP')
    ax.bar(x,             pseudo_lru_miss_rate, width, color='orange',     zorder=2, label='Pseudo-LRU')
    ax.bar(x + width,     mru_miss_rate,        width, color='green',      zorder=2, label='MRU')
    ax.bar(x + 2 * width, lfu_miss_rate,        width, color='hotpink',    zorder=2, label='LFU')
    ax.set_xticks(x, traces_names)
    ax.set_xlabel('Traces', fontsize=18)
    ax.set_ylabel('Miss Rate', fontsize=18)
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.legend()
    fig.tight_layout()
    plt.savefig(PICTURES_PATH + 'miss_rate_traces.pdf')
    plt.close()



def main():
    lru_stats        = parse_stats(LRU_JSON_PATH)
    drrip_stats      = parse_stats(DRRIP_JSON_PATH)
    pseudo_lru_stats = parse_stats(PSEUDO_LRU_JSON_PATH)
    mru_stats        = parse_stats(MRU_JSON_PATH)
    lfu_stats        = parse_stats(LFU_JSON_PATH)

    plot_stats(lru_stats, drrip_stats, pseudo_lru_stats, mru_stats, lfu_stats)


if __name__ == '__main__':
    main()
