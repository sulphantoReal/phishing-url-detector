# Phishing URL Detector

A machine learning classifier that predicts whether a URL is phishing or legitimate, using hand-engineered structural features (no deep learning, no pre-trained models) and scikit-learn.

## Why I built this

I'm working through the Google Cybersecurity Professional Certificate, and phishing detection kept coming up as a core analyst skill. At the same time I'm building a math foundation for AI/ML. This project sits right at that intersection so instead of reading about phishing indicators, I wanted to test which ones actually hold up as predictive signals when you build a real classifier and look at real data.

## How it works

1. **Dataset** — ~800,000 labeled URLs (phishing/legitimate) from a public Kaggle dataset, sampled down to a balanced 4,000 rows (2,000 each) for fast iteration. Author was Hari Krishna smthg.
2. **Feature engineering** — 9 features extracted from raw URL strings: length, dot count, hyphen count, slash count, digit count, presence of an IP address, presence of an `@` symbol, HTTPS usage, and presence of common phishing bait words (`login`, `verify`, `secure`, etc.).
3. **Modeling** — trained and compared two classifiers:
   - **Logistic Regression** (baseline) — 69.75% accuracy
   - **Random Forest** — 83% accuracy, and a much better balance of catching actual phishing URLs vs. false alarms

## Results

| Model | Accuracy | Phishing caught | Phishing missed |
|---|---|---|---|
| Logistic Regression | 69.75% | 218 / 402 | 184 |
| Random Forest | 83% | 325 / 402 | 77 |

Random Forest more than halved the number of missed phishing URLs compared to the baseline — the more important number for a security tool, since a missed phishing site is a worse failure than a false alarm on a safe one.

## What I learned

**My security intuition about which features "should" matter didn't fully match the data.** Before building this, I assumed classic phishing signals — IP addresses in the URL, `@` symbols, suspicious keywords — would dominate. The actual results were more nuanced:

- `has_ip_address` and `has_at_symbol`, the two most commonly cited phishing indicators, turned out to be nearly useless in this dataset (under 1.5% combined feature importance) — they were just too rare to matter across 4,000 samples.
- `has_suspicious_words` (keywords like "login," "verify," "secure") showed the single biggest gap between phishing and legitimate URLs when I compared class averages directly — phishing URLs contained these words about 70x more often. But in the final trained model, it ranked only 5th out of 9 features by importance.

That gap between "biggest average difference" and "most decisive in the model" was the most interesting finding of the whole project, and worth understanding rather than skipping past:

- **A feature can show a big difference between classes on average, while still being silent (zero) for most individual rows.** `has_suspicious_words` was 0 for 86% of phishing URLs — so while it's a strong signal *when it fires*, it only actively helps distinguish a minority of cases. Its dramatic average hides how rarely it actually applies.
- **A feature can also lose importance because another feature already covers the same ground, more consistently.** `count_slashes` and `url_length` ended up as the top two features by importance (27% and 22%) — likely because a URL with a deep, suspicious-looking path (which `count_slashes` captures) often also contains bait keywords, but slash count is *never* zero and applies to every single URL, while a keyword match only fires occasionally. Once the model had already split on structural features like slash count, the keyword feature had less new information left to add.

The takeaway: population-level averages (what a feature looks like *on average* across a whole class) and model-level importance (how much a feature actually swings individual decisions once combined with everything else) are answering different questions — and a feature can score high on one and low on the other. Checking both, instead of assuming they'd agree, was the useful part.

## Tech

Python, pandas, scikit-learn (`LogisticRegression`, `RandomForestClassifier`, `StandardScaler`, `train_test_split`).

## How to run it

1.`features.py` — the 9 feature-extraction functions themselves (`url_length`, `count_dots`, `has_ip_address`, etc.). Not run directly — imported by `build_features.py`.
2. `build_features.py` — loads the URL dataset, applies all 9 feature-extraction functions, saves `features_final.csv`
3. `train_model.py` — trains both models, prints accuracy and confusion matrices, prints feature importances

```bash
python build_features.py
python train_model.py
```
