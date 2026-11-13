# Validation record - 13 November 2026

## Files and execution

The supplied ZIP contained seven notebooks. All seven now validate against the notebook v4.5 schema. The originals contained invalid `outputs` properties on markdown cells; these were removed and stable cell IDs added.

Execution used Python 3.12 and IPython in-process, with a fresh namespace per notebook. Jupyter kernel execution was attempted but did not complete in this Windows environment. Successful execution therefore refers to the recorded in-process cell runs, not to an independent Jupyter kernel replay.

| Notebook | Outcome |
| --- | --- |
| 01 API | Partial. Static course JSON loaded. Live rockets enrichment returned HTTP 522. Error retained in the notebook. |
| 02 Scraping | Passed. 121 rows parsed from the fixed Wikipedia revision. Exhaustive semantic verification of table extraction was not performed. |
| 03 Wrangling | Passed. 90 rows. 60 successful and 30 unsuccessful labels. |
| 04 EDA | Passed. Seven PNG plots saved in the notebook and `images/`; numeric feature dataset exported. |
| 05 SQL | Passed. Ten query outputs saved in notebook and independently queried into `sql_results.json`. |
| 06 Folium | Passed. Interactive HTML generated. Railway/highway/city points remain unset, and coastline distance uses an illustrative point. Browser rendering was not visually verified. |
| 07 ML | Passed. Four complete grid searches, scores and six PNG figures saved. |

Per-notebook JSON records include duration and execution method. The failed API is not a successful end-to-end collection run. Subsequent notebooks use independently retrieved IBM snapshots, not a fabricated live API export.

## Corrections

- Classified outcomes by their semantic `True ` prefix instead of frequency-ranked indices.
- Moved normalization inside scikit-learn Pipeline, fitted within training folds.
- Stratified the 80/20 split, fixed random seeds and selected the model by training cross-validation score.
- Removed a duplicate SVM kernel candidate and fixed tree randomness.
- Removed repeated notebook dependency installation commands; dependencies are installed once from requirements.
- Used stable local dataset paths, bounded/cached API requests and SQL display configuration.
- Removed unused scraping dictionary keys that could produce empty columns; asserted nonempty extraction and equal column lengths.
- Added the missing Dash application, using the historical dashboard dataset.

scikit-learn 1.9.1 failed to load a native library under Windows application control. Version 1.7.2 loaded and completed the searches; that is the version pinned in requirements and recorded in the environment report.

## Independent checks

`python scripts/validate_project.py` passed: hashes for seven original downloaded sources, notebook schemas, all non-API execution counts/error outputs, binary labels, feature dimensions/missingness, score bounds, dashboard filtering for every site and three payload ranges (including empty subsets), page/layout/dependency endpoints and an actual callback HTTP response.

Dashboard validation is automated and does not include browser screenshots or visual interaction testing. The Folium HTML was generated but not browser-tested. Remote resources may be needed to display map tiles and browser libraries.

The modeling dataset has 90 records (72 train, 18 test). Decision tree mean CV accuracy was 0.8892857143; test accuracy was 0.8333333333 (15/18). SVM tied its test accuracy, but had a lower mean training CV score. The selected tree was chosen by CV. See `model_scores.csv` for all models.

No temporal holdout, operational point-in-time feature audit, uncertainty interval or external validation was performed. The course encoder uses the full historical data. These scores are retrospective educational evidence.

## Presentation

The original PPTX ZIP and its XML parts parse successfully and contain 38 slides. The original PDF parses and contains 38 pages; representative pages were rendered and inspected. The files contain explicit pending placeholders and have not been turned into a final assessment report.

`presentation/Execution_Evidence.pdf` is a separate 13-page evidence supplement. It includes actual plots and metrics and the repository URL. Its pages were rendered and visually reviewed. It explicitly states the remaining work and is not described as a complete Coursera submission.
