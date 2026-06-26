"""
Telco Customer Churn Analysis
Author: Vusal Mammadzade (GitHub: memmedzadev81-max)
Full EDA + Statistics + Statistical Tests + Business Insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ----------------------------------------------------------------------
# Global style
# ----------------------------------------------------------------------
sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 110
plt.rcParams["savefig.bbox"] = "tight"
PALETTE = {"No": "#4C9F70", "Yes": "#D9534F"}
IMG = "images/"

# ======================================================================
# 1. LOAD DATA
# ======================================================================
df = pd.read_csv("data/Telco-Customer-Churn.csv")
print("Shape:", df.shape)

# ======================================================================
# 2. DATA CLEANING
# ======================================================================
# TotalCharges is stored as text and has 11 blank values (new customers)
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
print("\nMissing TotalCharges after conversion:", df["TotalCharges"].isna().sum())

# These blanks belong to tenure = 0 customers -> total charge = 0
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# SeniorCitizen 0/1 -> readable
df["SeniorCitizen"] = df["SeniorCitizen"].map({0: "No", 1: "Yes"})

# Drop ID (not useful for analysis)
df = df.drop(columns=["customerID"])

# Duplicates check
print("Duplicate rows:", df.duplicated().sum())

# Churn rate
churn_rate = (df["Churn"] == "Yes").mean() * 100
print(f"\nOverall churn rate: {churn_rate:.1f}%")

# ======================================================================
# 3. EXPLORATORY DATA ANALYSIS (EDA)
# ======================================================================
print("\n--- Numeric summary ---")
print(df[["tenure", "MonthlyCharges", "TotalCharges"]].describe().round(2))

# ---- Figure 1: Churn balance (target distribution) ----
fig, ax = plt.subplots(figsize=(6, 4.5))
counts = df["Churn"].value_counts()
bars = ax.bar(counts.index, counts.values, color=[PALETTE["No"], PALETTE["Yes"]])
ax.set_title("Customer Churn Distribution", fontsize=13, weight="bold")
ax.set_ylabel("Number of customers")
for b, v in zip(bars, counts.values):
    ax.text(b.get_x() + b.get_width()/2, v + 40, f"{v}\n({v/len(df)*100:.1f}%)",
            ha="center", fontsize=10)
plt.savefig(IMG + "01_churn_distribution.png")
plt.close()

# ---- Figure 2: Tenure distribution by churn ----
fig, ax = plt.subplots(figsize=(8, 4.5))
for label in ["No", "Yes"]:
    sns.histplot(df[df["Churn"] == label]["tenure"], bins=30, label=f"Churn = {label}",
                 color=PALETTE[label], alpha=0.6, ax=ax)
ax.set_title("Tenure Distribution by Churn", fontsize=13, weight="bold")
ax.set_xlabel("Tenure (months)")
ax.legend()
plt.savefig(IMG + "02_tenure_by_churn.png")
plt.close()

# ---- Figure 3: Monthly charges by churn (boxplot) ----
fig, ax = plt.subplots(figsize=(6.5, 4.5))
sns.boxplot(data=df, x="Churn", y="MonthlyCharges", palette=PALETTE, ax=ax)
ax.set_title("Monthly Charges by Churn", fontsize=13, weight="bold")
plt.savefig(IMG + "03_monthlycharges_box.png")
plt.close()

# ---- Figure 4: Churn rate by Contract type ----
def churn_rate_by(col):
    return df.groupby(col)["Churn"].apply(lambda s: (s == "Yes").mean() * 100)

fig, ax = plt.subplots(figsize=(7, 4.5))
cr = churn_rate_by("Contract").sort_values(ascending=False)
bars = ax.bar(cr.index, cr.values, color="#D9534F")
ax.set_title("Churn Rate by Contract Type", fontsize=13, weight="bold")
ax.set_ylabel("Churn rate (%)")
for b, v in zip(bars, cr.values):
    ax.text(b.get_x()+b.get_width()/2, v+0.7, f"{v:.1f}%", ha="center", fontsize=10)
plt.savefig(IMG + "04_churn_by_contract.png")
plt.close()

# ---- Figure 5: Churn rate by Internet Service ----
fig, ax = plt.subplots(figsize=(7, 4.5))
cr = churn_rate_by("InternetService").sort_values(ascending=False)
bars = ax.bar(cr.index, cr.values, color="#E08E45")
ax.set_title("Churn Rate by Internet Service", fontsize=13, weight="bold")
ax.set_ylabel("Churn rate (%)")
for b, v in zip(bars, cr.values):
    ax.text(b.get_x()+b.get_width()/2, v+0.7, f"{v:.1f}%", ha="center", fontsize=10)
plt.savefig(IMG + "05_churn_by_internet.png")
plt.close()

# ---- Figure 6: Churn rate by Payment Method ----
fig, ax = plt.subplots(figsize=(9, 4.5))
cr = churn_rate_by("PaymentMethod").sort_values(ascending=False)
bars = ax.bar(cr.index, cr.values, color="#5B8DEF")
ax.set_title("Churn Rate by Payment Method", fontsize=13, weight="bold")
ax.set_ylabel("Churn rate (%)")
plt.xticks(rotation=15)
for b, v in zip(bars, cr.values):
    ax.text(b.get_x()+b.get_width()/2, v+0.7, f"{v:.1f}%", ha="center", fontsize=9)
plt.savefig(IMG + "06_churn_by_payment.png")
plt.close()

# ---- Figure 7: Correlation heatmap (numeric) ----
fig, ax = plt.subplots(figsize=(6, 5))
num = df[["tenure", "MonthlyCharges", "TotalCharges"]].copy()
num["Churn_flag"] = (df["Churn"] == "Yes").astype(int)
sns.heatmap(num.corr(), annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=ax)
ax.set_title("Correlation Heatmap", fontsize=13, weight="bold")
plt.savefig(IMG + "07_correlation_heatmap.png")
plt.close()

print("\nAll charts saved.")

# ======================================================================
# 4. STATISTICAL TESTS
# ======================================================================
print("\n" + "="*60)
print("STATISTICAL TESTS")
print("="*60)

results = {}

# ---- 4.1 Chi-square: Contract vs Churn ----
def chi_square(col):
    table = pd.crosstab(df[col], df["Churn"])
    chi2, p, dof, _ = stats.chi2_contingency(table)
    n = table.values.sum()
    cramers_v = np.sqrt(chi2 / (n * (min(table.shape) - 1)))
    return chi2, p, cramers_v

for col in ["Contract", "InternetService", "PaymentMethod", "TechSupport", "OnlineSecurity"]:
    chi2, p, v = chi_square(col)
    results[col] = (chi2, p, v)
    sig = "SIGNIFICANT" if p < 0.05 else "not significant"
    print(f"\nChi-square  {col} vs Churn:")
    print(f"  chi2 = {chi2:.2f} | p = {p:.2e} | Cramer's V = {v:.3f} -> {sig}")

# ---- 4.2 T-test: MonthlyCharges churn vs no-churn ----
g_yes = df[df["Churn"] == "Yes"]["MonthlyCharges"]
g_no  = df[df["Churn"] == "No"]["MonthlyCharges"]
t, p = stats.ttest_ind(g_yes, g_no, equal_var=False)
print(f"\nT-test  MonthlyCharges (Churn Yes vs No):")
print(f"  mean Yes = {g_yes.mean():.2f} | mean No = {g_no.mean():.2f}")
print(f"  t = {t:.2f} | p = {p:.2e} -> {'SIGNIFICANT' if p<0.05 else 'not significant'}")

# ---- 4.3 T-test: tenure churn vs no-churn ----
g_yes = df[df["Churn"] == "Yes"]["tenure"]
g_no  = df[df["Churn"] == "No"]["tenure"]
t, p = stats.ttest_ind(g_yes, g_no, equal_var=False)
print(f"\nT-test  tenure (Churn Yes vs No):")
print(f"  mean Yes = {g_yes.mean():.2f} | mean No = {g_no.mean():.2f}")
print(f"  t = {t:.2f} | p = {p:.2e} -> {'SIGNIFICANT' if p<0.05 else 'not significant'}")

# ---- 4.4 ANOVA: MonthlyCharges across Contract types ----
groups = [g["MonthlyCharges"].values for _, g in df.groupby("Contract")]
f, p = stats.f_oneway(*groups)
print(f"\nANOVA  MonthlyCharges across Contract types:")
print(f"  F = {f:.2f} | p = {p:.2e} -> {'SIGNIFICANT' if p<0.05 else 'not significant'}")

# ---- 4.5 Correlation: tenure vs TotalCharges ----
r, p = stats.pearsonr(df["tenure"], df["TotalCharges"])
print(f"\nPearson correlation  tenure vs TotalCharges:")
print(f"  r = {r:.3f} | p = {p:.2e}")

print("\nDONE.")
