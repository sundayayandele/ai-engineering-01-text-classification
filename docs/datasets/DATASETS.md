# Dataset governance

## Reference dataset
**SMS Spam Collection — UCI Machine Learning Repository**
- Dataset ID: 228
- Instances: 5,574
- Task: classification / clustering
- DOI: 10.24432/C5CC84
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Creators listed by UCI: Tiago Almeida and Jos Hidalgo

The repository does **not** commit the dataset. `scripts/train.py` retrieves it through `ucimlrepo`.

## Attribution
When publishing results derived from the corpus, cite the UCI dataset record and its associated publication as required by the dataset license.

## Governance
Record dataset version/retrieval date, split seed, preprocessing configuration and evaluation results for every promoted model. Do not mix production message content into retraining data without a lawful basis, retention policy and privacy/security review.
