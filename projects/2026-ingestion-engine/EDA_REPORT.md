# Presentation Resource: EDA Maturity Model & Statistical Deep Dive

This report contrasts the pedagogical divide between the **Student/Junior** track (`src/student/`) and the **Advanced/Enterprise** track (`src/enterprise/`). Use this as a guide to walk students through the move from "Code that Runs" to "Data that is Correct."

---

## 📊 Summary Statistics: The State of the Divide

| Metric | National Average | High-Connectivity Cluster | Low-Connectivity Cluster |
| :--- | :--- | :--- | :--- |
| **Reading Prof. (%)** | 42.5% | 51.2% | 33.1% |
| **Broadband Cov. (%)** | 81.0% | 94.2% | 62.4% |
| **AI Adoption (%)** | 12.5% | 18.2% | 6.4% |
| **Within-State SD** | 16.37 | 8.12 (Homogeneous) | 22.45 (Deeply Stratified) |

---

## 📑 Metric Glossary: What are we actually measuring?

To a Senior Engineer, a number is useless without its **contextual measure**.

| Measure | Definition | Why it Matters |
| :--- | :--- | :--- |
| **Pearson's R** | Measures the linear correlation between two variables (-1 to +1). | **Junior:** "Is there a line?" <br> **Senior:** "Is the line stable across subgroups?" |
| **Z-Score** | Measures how many standard deviations an observation is from the mean. | **Junior:** "Is this high or low?" <br> **Senior:** "Is this an outlier or a representative trend?" |
| **Inequality Index (StdDev)** | Measures the amount of variation or dispersion in a set of values. | **Junior:** Ignored (uses the Mean). <br> **Senior:** "How much did we destroy the truth by averaging these districts?" |
| **Cohen's d** | Measures the **Effect Size** (the magnitude of the difference between groups). | **Junior:** "The groups are different." <br> **Senior:** "Is the difference large enough to justify a $1B policy shift?" |

---

## 🧠 The Standpoint Contrast: Two Ways to See Data

| Data Point | Junior/Student Standpoint | Senior/Enterprise Standpoint |
| :--- | :--- | :--- |
| **r = 0.70** | "Success! Broadband predicts reading. Let's ship the model." | "Dangerous. Why is the correlation so high? Is it a proxy for wealth?" |
| **High StdDev** | "The data is a bit noisy, but the average looks okay." | "The average is a lie. The policy should be district-specific, not state-wide." |
| **Z-Score > 2.0** | "This state is doing great!" | "Is this state an anomaly in data reporting or a true success story?" |

---

## 🚀 The Path to Resolution: Ground Truth Reality

The Senior Pipeline **halts** because it detects **Simpson's Paradox** (Omitted Variable Bias). 

### The Blocker
When we look at the raw data, it seems Broadband Drives Reading. But when we **stratify** (group) by Infrastructure Tiers, the effect size decays. This suggests that a third "Lurking Variable" is driving both.

### The Resolution (Real Data)
We integrated the **Census ACS 1-Year Median Household Income** data to test the hypothesis.
1. **Raw Correlation:** 0.70
2. **Income-Adjusted Correlation:** 0.07 (Residual Analysis)
3. **The Conclusion:** Broadband is a *proxy* for wealth. If you give a poor district a faster modem without addressing the underlying economic and literacy support structures, the reading scores likely won't move.

> **🛡️ THE SENIOR VICTORY:**  
> Instead of shipping a biased model that promises "Broadband fixes literacy," you prove the **Wealth Confounder** with ground-truth data. You saved the business from a failed policy launch and moved the project toward a more comprehensive, multi-variable solution.
