# Telco Customer Churn

About **1 in 4** customers leave. This project finds who leaves, which factors matter, and what to fix first — with EDA and formal statistical tests on 7,043 customers.

Not a machine-learning model. The goal is clear segments and actions a commercial team can use.

---

## Business questions

1. What is the overall churn rate?
2. Which contract, payment and service groups churn more?
3. Are tenure and monthly charges different for leavers vs stayers?
4. Which changes would cut churn most?

---

## Dataset

| Item | Detail |
|------|--------|
| Source | IBM Telco Customer Churn sample |
| Rows | 7,043 |
| Target | `Churn` (Yes / No) |
| File | `data/Telco-Customer-Churn.csv` |

Cleaning: `TotalCharges` fixed (blank for tenure 0), `SeniorCitizen` mapped to Yes/No, `customerID` dropped.

---

## Stack

Python · pandas · matplotlib · seaborn · scipy · Jupyter

---

## Main findings

| Finding | Number |
|---------|--------|
| Overall churn | **26.5%** |
| Month-to-month contracts | **42.7%** vs 2.8% on 2-year |
| Electronic check payers | **45.3%** |
| Fiber optic | **41.9%** |
| No Tech Support / Online Security | ~**42%** each |
| Senior citizens | **41.7%** vs 23.6% |
| Leavers leave earlier | ~**18** months tenure vs ~38 |

### Tests (all significant at p < 0.05 where marked)

| Test | Result |
|------|--------|
| Contract × Churn (chi-square) | strong association (Cramér's V ≈ 0.41) |
| Internet / payment / tech support / security × Churn | p < 0.001 |
| Monthly charges: churn vs stay | higher for leavers |
| Tenure: churn vs stay | shorter for leavers |

---

## Recommendations

1. Push longer contracts — biggest single lever
2. Prefer auto-pay over electronic check
3. Focus onboarding in the first months
4. Bundle tech support and online security
5. Review fiber pricing/quality — high revenue, high churn

---

## Structure

```
Telco-Customer-Churn/
├── data/Telco-Customer-Churn.csv
├── notebooks/churn_analysis.ipynb
├── images/
├── analysis.py
├── requirements.txt
└── README.md
```

```bash
git clone https://github.com/memmedzadev81-max/Telco-Customer-Churn.git
cd Telco-Customer-Churn
pip install -r requirements.txt
python analysis.py
```

---

Vusal Mammadzade · [memmedzadev81-max](https://github.com/memmedzadev81-max)
