import os
import json
import numpy as np
import matplotlib.pyplot as plt


BIMODAL_JSON_PATH = '../branch/bimodal/json/'
MARKOV_JSON_PATH = '../branch/markov/json/'
MAKROV_PROBABILITY_JSON_PATH = '../branch/markov_probability/json/'
PICTURES_PATH = './pictures/'


class TraceStats:
    name: str
    ipc: float
    mpki: float


def gmean(iterable):
    return np.exp(np.log(iterable).mean())


def parse_file_stats(filename):
    info = TraceStats()
    info.name = os.path.basename(filename)

    with open(filename) as f:
        all_stats = json.load(f)
        roi_stats = all_stats[0]['roi']['cores'][0]

        cycles = float(roi_stats['cycles'])
        instructions = float(roi_stats['instructions'])
        mispredict = roi_stats['mispredict']

        info.ipc = instructions / cycles
        info.mpki = 1000 * sum(mispredict.values()) / instructions

    return info


def parse_stats(dirname):
    traces_stats = []
    for filename in os.listdir(dirname):
        stats = parse_file_stats(dirname + filename)
        traces_stats.append(stats)
    return traces_stats


def plot_stats(bimodal_stats, markov_stats, markov_probability_stats):
    bimodal_ipc = [stats.ipc for stats in bimodal_stats]
    bimodal_mpki = [stats.mpki for stats in bimodal_stats]

    markov_ipc = [stats.ipc for stats in markov_stats]
    markov_mpki = [stats.mpki for stats in markov_stats]

    markov_probability_ipc = [stats.ipc for stats in markov_probability_stats]
    markov_probability_mpki = [stats.mpki for stats in markov_probability_stats]

    bimodal_ipc_gmean = gmean(bimodal_ipc)
    bimodal_mpki_gmean = gmean(bimodal_mpki)

    markov_ipc_gmean = gmean(markov_ipc)
    markov_mpki_gmean = gmean(markov_mpki)

    markov_probability_ipc_gmean = gmean(markov_probability_ipc)
    markov_probability_mpki_gmean = gmean(markov_probability_mpki)

    predictor_names = [
        "Bimodal",
        "Markov",
        "Markov Probability"
    ]

    predictor_ipc_gmean = [
        bimodal_ipc_gmean,
        markov_ipc_gmean,
        markov_probability_ipc_gmean
    ]

    predictor_mpki_gmean = [
        bimodal_mpki_gmean,
        markov_mpki_gmean,
        markov_probability_mpki_gmean
    ]

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    fig.suptitle('Instructions Per Cycle', fontsize=20)
    ax.grid(zorder=0)
    ax.set_xlabel('Predictor', fontsize=18)
    ax.set_ylabel('IPC', fontsize=18)
    ax.tick_params(axis='both', which='major', labelsize=14)
    rects = ax.bar(predictor_names, predictor_ipc_gmean, align='center', zorder=2)
    ax.bar_label(rects, padding=2, fontsize=16)
    ax.set_ylim([0, 1])
    plt.savefig(PICTURES_PATH + 'ipc_gmean.pdf')
    ax.set_ylim([0.8, 1])
    plt.savefig(PICTURES_PATH + 'ipc_gmean_zoomed.pdf')
    plt.close()

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    fig.suptitle('Mispredictions Per Kilo Instruction', fontsize=20)
    ax.grid(zorder=0)
    ax.set_xlabel('Predictor', fontsize=18)
    ax.set_ylabel('MPKI', fontsize=18)
    ax.tick_params(axis='both', which='major', labelsize=14)
    rects = ax.bar(predictor_names, predictor_mpki_gmean, align='center', zorder=2)
    ax.bar_label(rects, padding=2, fontsize=16)
    plt.savefig(PICTURES_PATH + 'mpki_gmean.pdf')
    plt.close()



def main():
    bimodal_stats = parse_stats(BIMODAL_JSON_PATH)
    markov_stats = parse_stats(MARKOV_JSON_PATH)
    markov_probability_stats = parse_stats(MAKROV_PROBABILITY_JSON_PATH)

    plot_stats(bimodal_stats, markov_stats, markov_probability_stats)


if __name__ == '__main__':
    main()
