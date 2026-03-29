# Digital Divide Ingestion Engine

### MSU Denver — Guest Lecture (CS 3120) — April 9th, 2026

Welcome to the **Digital Divide Ingestion Engine**. This repository is a real-world data engineering case study exploring the intersection of infrastructure (**Broadband**), adoption (**AI Tools**), and student outcomes (**Grade 3 Reading Proficiency**).

This is not a single codebase; it is a **Maturity Model**. It is designed to be explored in two "strata": the **Foundational/Student** path and the **Advanced/Enterprise** path.

---

## 🍎 Educator's Curriculum Mapping (MSU Denver)

This repository is designed as a reusable pedagogical asset mapped to the **Metropolitan State University of Denver (MSU Denver)** Computer Science and Data Science & Machine Learning (DSML) programs. 

> **🛡️ IMPORTANT DISCLOSURE:**  
> This mapping is based on the 2024-2025 MSU Denver Academic Catalog. Educators at other institutions should refer to their specific student learning objectives (SLOs) and internal accreditation requirements for appropriate re-use and credit.

### Course-Specific Integration Points

| Course ID | Course Title | Mapping & Learning Objectives |
| :--- | :--- | :--- |
| **CS 3120** | Machine Learning | **Objectives 1, 4, & 9:** Students can use `senior_eda.py` to evaluate appropriate ML techniques, analyze models reflecting real-world data, and explore hidden patterns vs. bias. |
| **CS 3250** | SW Dev Methods | **Objectives 4 & 5:** Students can explore the `tests/` suite for TDD/BDD environments and analyze static/dynamic program properties across the two tracks. |
| **CS 3810** | Principles of DB | **Objectives 4 & 5:** Students can investigate the Medallion Architecture (Bronze/Silver/Gold) in `sql/` and practice writing complex DuckDB queries. |
| **DSML 2120**| Data Visualization | **Communication:** Students can adapt the `eda.py` plotting logic to communicate data-driven insights effectively using `matplotlib` and `seaborn`. |
| **MTH 3270**| Data Science | **Foundations:** This codebase provides a full-lifecycle example of data mining, from landing zone ingestion to stratified statistical analysis. |

### Pedagogical Pivot Points for Professors
* **The "Senior" Halt:** Use the `Simpson's Paradox` check in the Enterprise track to teach students that "code that runs" is not the same as "data that is correct."
* **Architectural Evolution:** Contrast the procedural Python in `src/student/` with the declarative, decoupled YAML logic in `src/enterprise/`.
* **Cross-Platform Engineering:** Discuss the shift from `os.path` (manual string handling) to `pathlib` (object-oriented) for production reliability.


## 🛠️ Environment Setup

1. **Python Selection:** Ensure you have Python 3.10+<sup>[1](#footnote-1)</sup> installed.
2. **Virtual Environment:** 
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # OR: venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
3. **API Keys (Production Only):**
   Copy `.env.example` to `.env` and provide your Census/FCC keys if you wish to run the **Live Ingestion Layer**.
   ```bash
   cp .env.example .env
   ```

---

## 🚀 Quick Start (5-Minute Onboarding)

*Ready to run the pipeline right now? Use these copy-paste commands to verify your environment.*

### 1. Verify the Entire Student Suite (22 Tests)
```bash
pytest tests/student/ -v
```

### 2. Run the Student "Dev Mode" Pipeline (No API keys needed)
```bash
python src/student/run_student.py --env dev
```

### 3. Run the Enterprise "Engine" (Demonstrating Scalability)
You can run the full engine or a lightweight single-job config:
```bash
# Full run
python -m src.enterprise.run_enterprise
# Lightweight job demonstration
python -m src.enterprise.run_enterprise --config src/enterprise/configs/nces_light.yaml
```

---

## ❓ Troubleshooting (FAQ)

### 1. `ModuleNotFoundError: No module named 'src'`
**Cause:** Your `PYTHONPATH` isn't seeing the project root.
**Fix:** Always run your commands from the root directory (`2026-ingestion-engine/`) and use the `-m` flag for the Enterprise track: `python -m src.enterprise.run_enterprise`.

### 2. `duckdb.CatalogException: Cannot open database file`
**Cause:** DuckDB only allows one process to open a database file at a time.
**Fix:** Close any other Python scripts or Database GUIs (like DBeaver or DuckDB CLI) that are currently looking at the `.duckdb` files in the `data/` folder.

### 3. `401 Unauthorized` or `403 Forbidden`
**Cause:** You are running in `--env prod` but your `.env` file is missing or contains incorrect credentials.
**Fix:** Copy `.env.example` to `.env`. For class demonstrations, stick to `--env dev` which uses local fixture files.

### 4. Path Errors on Windows (Backslash vs. Slash)
**Cause:** Windows uses `\` while Unix uses `/`. 
**Fix:** The code uses `pathlib` (Enterprise) and `os.path.join` (Student) to handle this automatically. If you see a path error, ensure you are running in a modern terminal like **PowerShell** or **Zsh**.

---

## 🛤️ Choose Your Learning Track

### 1. The Student Track (`src/student/`)
**Mindset:** "How do I make this work using the libraries I've learned?"
*   Exposed Python scripts for each API collector.
*   Explicit, procedural transformations.
*   Simple Pearson-based EDA (`eda.py`).
*   **Run it:** 
    ```bash
    python src/student/run_student.py --env dev
    ```

### 2. The Enterprise Track (`src/enterprise/`)
**Mindset:** "How do I make this resilient, scalable, and statistically valid for a Fortune 500 company?"
*   Declarative architecture (YAML-based ingestion contracts).
*   Abstract Base Clients & Custom Plugins.
*   Cross-platform object-oriented pathing (`pathlib`).
*   **Senior EDA Gatekeeper:** Rigorous Simpson's Paradox and Omitted Variable Bias checks.
*   **Run it:** 
    ```bash
    python -m src.enterprise.run_enterprise
    ```

---

## 🧠 The Senior Mindset (Career Advice)

If you are a student graduating soon, the mechanical ability to write a `requests.get()` call is only the "entry fee." To become an **Individual Contributor (IC)** at a major tech firm, your evolution looks like this:

| Junior Phase (Foundations) | Senior Phase (Architectural) |
| :--- | :--- |
| **"Make it run."** | **"Make it maintainable."** (What happens in 2 years?) |
| **"Trust the API."** | **"The API lies."** (Detecting data poison before model loading.) |
| **"Correlation = Result"** | **"Control for Confounders"** (Simpson's Paradox detection.) |
| **Absolute Unix Paths** | **Platform-Agnostic logic** (Win/Mac/Linux compliance.) |

**The Takeaway:**
When you explore this repo, look at the difference between `src/student/eda.py` (which ships everything) and `src/enterprise/senior_eda.py` (which purposefully **halts** the pipeline when it finds a statistical flaw). A Junior analyst gives the business a number; a Senior engineer gives the business an **insurance policy**.

---

## 📚 Resources
*   [LECTURE_NOTES.md](LECTURE_NOTES.md) — The complete presentation script & Medallion architecture diagrams.
*   [EDA_REPORT.md](EDA_REPORT.md) — The "Grand Finale" contrast guide comparing track outcomes.

*Good luck with your data mining journey!*

---

## 📄 Licensing

This repository is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license. 

*   **Attribution:** You must give appropriate credit to the original author.
*   **Non-Commercial:** You may not use this material for commercial purposes or paid course packages.
*   **ShareAlike:** If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

See the [LICENSE](LICENSE) file for the full legal text.

---

<a name="footnote-1"></a>
**[1] Why 3.10+?** This codebase leverages modern Python features including **Union Type Hinting** (`X | Y` syntax), performance optimizations for large-scale data processing, and native compatibility with the latest `duckdb` and `pandas` releases.
