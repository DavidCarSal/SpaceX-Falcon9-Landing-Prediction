# Validation record - final submission version, 13 November 2026

## Final presentation

The final report is `presentation/Data Science Capstone Project Report.pdf`: 40 slides in English, exported from Microsoft PowerPoint for Microsoft 365 using standard PDF output. The corresponding editable PPTX opened in PowerPoint successfully. The final PDF has searchable text, David Carro Salinas as author and a working repository hyperlink. Every PDF page was rendered and reviewed individually. No RUN REQUIRED, ADD YOUR or repository-result placeholders remain in the final report.

The PPTX passed package integrity, layout/font checks and first-party re-import. All encoded slide text uses the source Aptos font. File hashes and the page-review record are in `final_presentation_validation.json`.

The earlier drafts and 13-page preliminary supplement are preserved in `presentation/archive/` and superseded. Their pending-result statements refer to that earlier stage. They are not the submission file.

## Notebooks and execution

All seven notebooks validate against notebook schema v4.5. Invalid outputs properties on markdown cells were removed and stable cell IDs added. Execution used Python 3.12 and IPython in-process, with a fresh namespace per notebook. An attempted Jupyter kernel execution did not complete in this Windows environment; successful execution refers to the recorded in-process cell runs.

| Notebook | Outcome |
| --- | --- |
| 01 API | Partial. Course JSON loaded; live rockets enrichment returned HTTP 522. Error retained. |
| 02 Scraping | Passed. 121 parsed rows from a fixed Wikipedia revision. Exhaustive merged-cell semantic validation was not performed. |
| 03 Wrangling | Passed. 90 records, 60 successful and 30 unsuccessful labels. |
| 04 EDA | Passed. Seven saved figures; numeric flight axes improved for readability; encoded features exported. |
| 05 SQL | Passed. Ten executed queries; Mission_Outcome is trimmed before grouping. |
| 06 Folium | Passed. Maps generated, sourced proximity coordinates included, consistent Earth radius used. |
| 07 ML | Passed. Four complete grid searches, scores and six figures saved. |

Per-notebook JSON records include duration and execution method. The API failure is not counted as successful end-to-end collection. Subsequent analysis uses independently downloaded IBM snapshots.

## Corrections and reproducibility

- Outcome labels use the semantic True prefix, rather than frequency-ranked indices.
- StandardScaler runs inside a Pipeline, fitted within each training CV fold.
- The 80/20 split is stratified. Model selection uses mean training CV accuracy, with fixed split and tree random seeds.
- Duplicate SVM kernel candidates were removed, local dataset paths standardized and repeated dependency installation cells replaced with one requirements file.
- API requests are bounded and cached. Scraping requires nonempty extraction and equally sized columns.
- The missing Dash application was implemented and tested.
- The original downloads remain byte-for-byte preserved; Git attributes protect dataset hashes and PDF bytes from newline conversion.

scikit-learn 1.9.1 encountered a native-library loading error under Windows application control. Version 1.7.2 loaded and completed the searches. The executed version is pinned and recorded in `environment.json`.

## Results and limits

The modeling dataset contains 90 records, with 72 training and 18 test cases. The decision tree achieved mean training CV accuracy 0.8892857143 and test accuracy 0.8333333333 (15/18). SVM tied the test accuracy but had a lower mean CV score. The selected tree has TN=3, FP=3, FN=0, TP=12; specificity on unsuccessful outcomes is 50%.

The evaluation is retrospective and small. No temporal holdout or operational point-in-time feature audit was performed. The course encoder and imputed inputs use the historical dataset; these scores do not establish prospective flight performance. The report states these limitations.

## Geographic evidence

The saved Overpass query returned mapped coastlines, railway lines and selected major-road classes within 15 km of the approximate course site coordinate, plus town/city nodes within 50 km. The raw response, timestamp, source object IDs and hash are preserved.

Nearest points on returned way segments were approximated in a local projection and measured with the spherical great-circle formula, using R=6371.0088 km. Distances are 0.92 km to mapped coastline, less than 0.01 km to a mapped rail spur, 6.38 km to the selected major road (NASA Parkway East, secondary/private) and 19.56 km to the Cape Canaveral mapped centre. These are not travel distances, survey-grade measurements or historical launch-year infrastructure data.

Folium browser captures include national context, Florida outcomes and proximity views. The outcome detail view applies disclosed display-only offsets to coincident markers; the offsets are never used in distance calculations. Map tiles and data are attributed to OpenStreetMap contributors.

## Dashboard and independent checks

Automated checks cover all sites, three payload ranges including empty subsets, layout/dependency endpoints and an actual Dash callback HTTP response. Microsoft Edge browser checks clicked the KSC option, moved the slider with the keyboard and captured actual rendered states for all sites, KSC and a 2,000-5,000 kg range.

`python scripts/validate_project.py` checks source hashes, seven notebook schemas, six successful execution records, labels, features, four score rows, dashboard callbacks, OSM provenance and the final 40-page PDF / 40-slide PPTX, author and repository link. It does not re-execute the notebooks or guarantee a grade.
