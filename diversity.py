#!/usr/bin/env python3

#!/usr/bin/env python3

"""Maximum similarity to an ideal ranking from files in TREC format

This script implements the *diversification* version of an evaluation
metric called "compatibility", which was developed and explored
over three papers (below).  If you want to read about the measure
generally, we suggest starting with the first paper (i.e. most
recent). However, this code supports the second paper. Unless you
are specifically interested in diversity, you proably want the
script at:
https://github.com/claclark/Compatibility/blob/master/compatibility.py

1) Charles L. A. Clarke, Alexandra Vtyurina, and Mark D. Smucker. 2020.
   Assessing top-k preferences
   Under review. See: https://arxiv.org/abs/2007.11682

2) Charles L. A. Clarke, Mark D. Smucker, and Alexandra Vtyurina. 2020.
   Offline evaluation by maximum similarity to an ideal ranking.
   29th ACM Conference on Information and Knowledge Management.

3) Charles L. A. Clarke, Alexandra Vtyurina, and Mark D. Smucker. 2020.
   Offline evaluation without gain.
   ACM SIGIR International Conference on the Theory of Information Retrieval.

"""

import argparse
import sys

# Default persistence of 0.95, which is roughly equivalent to NSCG@20.
# Can be changed on the command line.
P = 0.95

# Depth for RBO computation. There's probably no need to ever play with this.
DEPTH = 100


def rbo(run, ideal, p):
    run_set = set()
    ideal_set = set()
    depth = min(DEPTH, max(len(run), len(ideal)))

    score = 0.0
    normalizer = 0.0
    weight = 1.0
    for i in range(depth):
        if i < len(run):
            run_set.add(run[i])
        if i < len(ideal):
            ideal_set.add(ideal[i])
        score += weight*len(ideal_set.intersection(run_set))/(i + 1)
        normalizer += weight
        weight *= p
    return score/normalizer


def prioritize(count, available):
    top = 10000000
    for subtopic in count:
        if count[subtopic] < available[subtopic] and top > count[subtopic]:
            top = count[subtopic]
    priorities = {}
    for subtopic in count:
        if count[subtopic] != available[subtopic] and count[subtopic] == top:
            priorities[subtopic] = 1
        else:
            priorities[subtopic] = 0
    return priorities


def compute_score(subtopics, priorities):
    score = 0.0
    for subtopic in subtopics:
        score += priorities[subtopic]
    return score


def idealize(topic, qrels, run):
    rank = {}
    for i in range(len(run)):
        rank[run[i]] = i

    subtopics = set()
    for docno in qrels:
        subtopics |= qrels[docno]
    count = {}
    available = {}
    for subtopic in subtopics:
        count[subtopic] = 0
        available[subtopic] = 0
    for docno in qrels:
        for subtopic in qrels[docno]:
            available[subtopic] += 1

    ideal = []
    included = set()
    remaining = []
    for docno in qrels:
        remaining.append(docno)
    while len(ideal) < len(qrels):
        remaining.sort(
            key=lambda docno: rank[docno] if docno in rank else len(run))
        priorities = prioritize(count, available)
        scores = {}
        for docno in remaining:
            scores[docno] = compute_score(qrels[docno], priorities)
        remaining.sort(key=lambda docno: scores[docno], reverse=True)
        best = remaining[0]
        remaining = remaining[1:]
        ideal.append(best)
        for subtopic in qrels[best]:
            count[subtopic] += 1
    return ideal


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', type=float, default=P, help='persistence')
    parser.add_argument('qrels', type=str, help='TREC-style qrels')
    parser.add_argument('run', type=str, help='TREC-style run')
    args = parser.parse_args()

    if args.p < 0.01 or args.p > 0.99:
        print('Value of p = ' + str(args.p) + ' out of range [0.01,0.99]',
              file=sys.stderr)
        sys.exit(0)

    qrels = {}
    with open(args.qrels) as qrelsf:
        for line in qrelsf:
            (topic, subtopic, docno, qrel) = line.rstrip().split()
            qrel = float(qrel)
            if qrel > 0.0:
                if topic not in qrels:
                    qrels[topic] = {}
                if docno not in qrels[topic]:
                    qrels[topic][docno] = set()
                qrels[topic][docno].add(subtopic)

    runid = ""
    run = {}
    scores = {}
    with open(args.run) as runf:
        for line in runf:
            (topic, q0, docno, rank, score, runid) = line.rstrip().split()
            if topic not in run:
                run[topic] = []
                scores[topic] = {}
            run[topic].append(docno)
            scores[topic][docno] = float(score)

    for topic in run:
        run[topic].sort()
        run[topic].sort(key=lambda docno: scores[topic][docno], reverse=True)

    ideal = {}
    for topic in run:
        if topic in qrels:
            ideal[topic] = idealize(topic, qrels[topic], run[topic])

    print('runid', 'topic', 'compatibility', sep=',')
    count = 0
    total = 0.0
    for topic in run:
        if topic in ideal:
            score = rbo(run[topic], ideal[topic], args.p)
            count += 1
            total += score
            print(runid, topic, score, sep=',')

    if count > 0:
        print(runid, 'average', total/count, sep=',')
    else:
        print(runid, 'average', 0.0, sep=',')
