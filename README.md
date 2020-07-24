# Compatibility
Offline evaluation by maximum similarity to an ideal ranking

This code implements a search evaluation metric called "compatibility", which
was developed and explored over three papers.  Start with the first
(i.e., the most recent) for the best explanation.

1) Charles L. A. Clarke, Alexandra Vtyurina, and Mark D. Smucker. 2020.
   Assessing top-k preferences
   Under review. See: https://arxiv.org/abs/2007.11682

2) Charles L. A. Clarke, Mark D. Smucker, and Alexandra Vtyurina. 2020.
   Offline evaluation by maximum similarity to an ideal ranking.
   29th ACM Conference on Information and Knowledge Management.

3) Charles L. A. Clarke, Alexandra Vtyurina, and Mark D. Smucker. 2020.
   Offline evaluation without gain.
   ACM SIGIR International Conference on the Theory of Information Retrieval.

Formats are backward compatible with the standard formats used by TREC for
adhoc runs and relevance judgments. However, the "qrels" file expresses preferences rather than graded relevance values.
Preferences can be any positive floating point or integer value.
If one document's preference value is greater than another document's
preference value, it indicates that the first document is preferred over the second.
If preferences are tied, it indicates that the two documents are equally preferred.
See TREC-CAsT-2019.qrels for an example.
