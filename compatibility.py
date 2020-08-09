#!/usr/bin/env python3

"""Maximum similarity to an ideal ranking from files in TREC format

This code implements an evaluation metric called "compatibility", which
was developed and explored over three papers.  Start with the first
(i.e. most recent).

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

# An additional normalization step was introduced in paper #1 (above)
# to handle short, truncated ideal results.  I don't recommend changing
# it, so it's not an command line argument, but setting it to False
# is required to exactly reproduce the numbers in papers #2 and #3,
# as well as the un-normalized numbers in paper #1.
NORMALIZE = True

# Depth for RBO computation. There's probably no need to ever play with this.
DEPTH = 1000


def rbo(run, ideal, p):
    run_set = set()
    ideal_set = set()

    score = 0.0
    normalizer = 0.0
    weight = 1.0
    for i in range(DEPTH):
        if i < len(run):
            run_set.add(run[i])
        if i < len(ideal):
            ideal_set.add(ideal[i])
        score += weight*len(ideal_set.intersection(run_set))/(i + 1)
        normalizer += weight
        weight *= p
    return score/normalizer


def idealize(run, ideal, qrels):
    rank = {}
    for i in range(len(run)):
        rank[run[i]] = i
    ideal.sort(key=lambda docno: rank[docno] if docno in rank else len(run))
    ideal.sort(key=lambda docno: qrels[docno], reverse=True)
    return ideal


def main():
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

    ideal = {}
    qrels = {}
    with open(args.qrels) as qrelsf:
        for line in qrelsf:
            (topic, q0, docno, qrel) = line.rstrip().split()
            qrel = float(qrel)
            if qrel > 0.0:
                if topic not in qrels:
                    ideal[topic] = []
                    qrels[topic] = {}
                if docno in qrels[topic]:
                    if qrel > qrels[topic][docno]:
                        qrels[topic][docno] = qrel
                else:
                    ideal[topic].append(docno)
                    qrels[topic][docno] = qrel

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
        if topic in ideal:
            ideal[topic] = idealize(run[topic], ideal[topic], qrels[topic])

    print('runid', 'topic', 'compatibility', sep=',')
    count = 0
    total = 0.0
    for topic in run:
        if topic in ideal:
            score = rbo(run[topic], ideal[topic], args.p)
            if NORMALIZE:
                best = rbo(ideal[topic], ideal[topic], args.p)
                if best > 0.0:
                    score /= best
                else:
                    score = best
            count += 1
            total += score
            print(runid, topic, score, sep=',')

    if count > 0:
        print(runid, 'average', total/count, sep=',')
    else:
        print(runid, 'average', 0.0, sep=',')

if __name__ == "__main__":
    main()
