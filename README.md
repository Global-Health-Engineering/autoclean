<!-- badges: start -->
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18656175.svg)](https://doi.org/10.5281/zenodo.18656175)
<!-- badges: end -->

# AutoClean

Modular data cleaning functions with Large Language Model (LLM) integration, developed as part of a bachelor thesis at the [Global Health Engineering](https://ghe.ethz.ch/) group, ETH Zurich.

## About

AutoClean is a set of eight data cleaning functions that can operate independently or be combined into a configurable pipeline, complemented by a report generation module that documents every cleaning step and its parameters. The functions cover preprocessing, duplicate detection, statistical and semantic outlier detection, datetime standardization, structural error correction, missing value imputation, and postprocessing. Some functions rely on purely algorithmic approaches, while others integrate LLMs for tasks that require semantic understanding.

A particular focus of this project is the structural error correction function, which uses clustering to group inconsistent representations of the same entity into a single canonical form. Its multi-pass strategy combines character-level, semantic, and context-aware similarity methods to handle diverse column types.

For a detailed description of the methods, evaluation, and results, see the accompanying thesis.

## Repository Structure

```
AutoClean/
├── Functions/                        # Core cleaning modules
│   ├── Pre_Processing.py             # Data loading and initial cleanup
│   ├── Duplicates.py                 # Duplicate row and column detection
│   ├── Semantic_Outliers.py          # LLM-based semantic outlier detection
│   ├── Outliers.py                   # Statistical outlier detection (IQR)
│   ├── DateTime_Standardization.py   # Date format standardization
│   ├── Structural_Errors.py          # Structural error correction (main function)
│   ├── Missing_Values.py             # Missing value imputation (including KNN, MissForest)
│   ├── Post_Processing.py            # Final export and formatting
│   ├── Cleaning_Report.py            # Markdown report generation
│   └── Structural_Errors_Helper/     # Helper modules for structural errors
│       ├── Similarity.py             # Similarity computation (RapidFuzz, Embeddings, LLM)
│       ├── Clustering.py             # Clustering (Hierarchical, Connected Components, Affinity Propagation)
│       └── Canonical.py              # Canonical form selection (most frequent, LLM)
├── Data/                             # Datasets used for evaluation
│   ├── Test/                         # Simulated WASH dataset with intentional data quality issues
│   ├── Salary/                       # Self-reported salary survey data
│   └── Drilling/                     # Borehole drilling and construction data from Malawi
├── Additional_Information/           # Algorithm documentation
├── Script_Test.py                    # Evaluation script for simulated WASH dataset (demonstrates full pipeline)
├── Script_Salary.py                  # Evaluation script for Salary dataset
├── Script_Drilling.py                # Evaluation script for Drilling dataset
├── CITATION.cff                      # Citation metadata
└── LICENSE                           # MIT License
```

Each dataset folder contains the original CSV, the cleaned CSV, and the generated cleaning report in both Markdown and PDF format. The Test folder additionally contains `Generate_Correlated_Columns.py`, which was used to generate columns with known correlations for evaluating the missing value imputation function.

## Requirements

- Python 3.12+
- An OpenAI API key (required for LLM-based functions)

### Dependencies

```
pandas
numpy
scikit-learn
scipy
rapidfuzz
pyjanitor
openai
pydantic
python-dotenv
python-dateutil
```

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/Global-Health-Engineering/autoclean.git
cd autoclean
```

2. Install the dependencies:

```bash
pip install pandas numpy scikit-learn scipy rapidfuzz pyjanitor openai pydantic python-dotenv python-dateutil
```

3. Create a `.env` file in the project root with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

4. Run one of the evaluation scripts to see the pipeline in action:
```bash
python Script_Test.py
```
Alternatively, the functions can be imported individually and used on your own datasets. See the evaluation scripts for usage examples.

## Datasets

| Dataset | Description | Source |
|---------|-------------|--------|
| `Test.csv` | Simulated WASH dataset with intentional data quality issues | Generated for this thesis |
| `Salary.csv` | Self-reported salary survey data (28,187 rows) | [Ask A Manager](https://www.askamanager.org/2021/04/how-much-money-do-you-make-4.html) |
| `Drilling.csv` | Borehole drilling and construction data from Malawi (157 rows) | [openwashdata](https://github.com/openwashdata/drillingdata) |

## Citation

Please cite this repository as:

> Seiler, F., Massari, N., Tkaczuk, J., & Tilley, E. (2026, February). *AutoClean: Modular Data Cleaning Functions with Large Language Model Integration - Software* (Version 0.0.1). https://doi.org/10.5281/zenodo.18656175

## License

This project is licensed under the [MIT License](LICENSE).

## Authors

- **Florin Seiler** — development and thesis — [seilerf@ethz.ch](mailto:seilerf@ethz.ch)
- **Nicolò Massari** — supervision — [nicolo.massari@lam.fr](mailto:nicolo.massari@lam.fr)
- **Jakub Tkaczuk** — supervision — [jtkaczuk@ethz.ch](mailto:jtkaczuk@ethz.ch)
- **Elizabeth Tilley** — supervision — [tilleye@ethz.ch](mailto:tilleye@ethz.ch)

[Global Health Engineering](https://ghe.ethz.ch/), ETH Zurich