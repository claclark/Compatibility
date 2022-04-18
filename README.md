# Compatibility
Offline evaluation by maximum similarity to an ideal ranking.

This is my main hub for this project. Start by reading paper #4.

1) Negar Arabzadeh, Alexandra Vtyurina, Xinyi Yan, and Charles L. A. Clarke.
   Shallow pooling for sparse labels. *Under review*.
     * Paper: https://arxiv.org/abs/2109.00062
     * Data: https://github.com/Narabzad/Shallow-Pooling-for-Sparse-labels

3) Xinyi Yan, Chengxi Luo, Charles L. A. Clarke, Nick Craswell, and Ellen M. Voohees, and Pablo Castells. 2022.
   Human Preferences as Dueling Bandits.
   45th International ACM SIGIR Conference on Research and Development in Information Retrieval.
     * Code and data: https://github.com/XinyiYan/duelingBandits
     * More code: https://github.com/claclark/preferences

3) Chengxi Luo, Charles L. A. Clarke and Mark D. Smucker. 2021.
   Evaluation measures based on preference graphs.
   44th International ACM SIGIR Conference on Research and Development in Information Retrieval.
     * Paper: https://dl.acm.org/doi/abs/10.1145/3404835.3462947
     * Code: https://github.com/chengxiluo/Evaluation-Measures-based-on-Preference-Graphs
     * More code: https://github.com/claclark/preferences

4) Charles L. A. Clarke, Alexandra Vtyurina, and Mark D. Smucker. 2021.
   Assessing top-k preferences.
   ACM Transactions on Information Systems.
     * Paper: https://arxiv.org/abs/2007.11682
     * Data: this repo (see below for details)
     * Code: https://github.com/claclark/preferences

5) Charles L. A. Clarke, Mark D. Smucker, and Alexandra Vtyurina. 2020.
   Offline evaluation by maximum similarity to an ideal ranking.
   29th ACM Conference on Information and Knowledge Management.
     * Paper: https://dl.acm.org/doi/10.1145/3340531.3411915
     * Code: this repo (see below for details)

6) Charles L. A. Clarke, Alexandra Vtyurina, and Mark D. Smucker. 2020.
   Offline evaluation without gain.
   ACM SIGIR International Conference on the Theory of Information Retrieval.
     * Paper: https://dl.acm.org/doi/10.1145/3409256.3409816
   
The script ``compatibility.py`` implements a search evaluation metric called "compatibility", which was first developed and explored in papers #4-6.
Formats are backward compatible with the standard formats used by TREC for adhoc runs and relevance judgments.
However, the "qrels" file expresses preferences rather than graded relevance values.
Preferences can be any positive floating point or integer value.
If one document's preference value is greater than another document's preference value, it indicates that the first document is preferred over the second.
If preferences are tied, it indicates that the two documents are equally preferred.
See TREC-CAsT-2019.qrels for an example.

Data files for paper #4:
* ``TREC-CAsT-2019.pref``': Crowdsourced preference judgments
* ``TREC-CAsT-2019.qrels``: Combined qrels based on the crowdsourced preference judgments and the original graded judgments
* ``TREC-CAST-2019.local.pref``: Local preference judgments
* ``TREC-CAsT-2019.local.qrels``: Top-1 qrels based on the local preference judgments

The script ``divesity.py`` implements a version of compatibility from paper #5 that incorporates a notion of diversity.
It interprets qrels differently than the script above, so be aware.

We are happy to answer any and all questions.
