-- =============================================================
-- gold_digital_divide.sql
-- Gold Layer: Digital Divide Feature Table
--
-- Three-way JOIN: NCES EDFacts × FCC Broadband × Census HPS
-- Grain: State × Year
-- Target Variable (y): reading_pct_proficient
--
-- Engineering notes:
--   1. District-level NCES data is aggregated to state grain using a
--      STUDENT-COUNT-WEIGHTED average (not a naive mean) to avoid
--      small-district bias. This is a deliberate, documented choice.
--   2. The `all_students_flag` filter isolates the "All Students"
--      aggregate rows (EDFacts subgroup code 99) before aggregation.
--   3. NULLIF guards prevent division-by-zero on states with suppressed data.
--   4. Window function (AVG OVER PARTITION BY year) computes the national
--      weighted mean dynamically — no hardcoded constant.
--   5. FIPS join: NCES stores fips as INTEGER; FCC/HPS store as VARCHAR.
--      Explicit CAST ensures the join succeeds without silent type coercion.
-- =============================================================

-- ANSI SQL:2003 compliant: DROP + CREATE instead of proprietary CREATE OR REPLACE
-- Portable across PostgreSQL, Snowflake, BigQuery, Redshift, and DuckDB.
DROP TABLE IF EXISTS gold_digital_divide;

CREATE TABLE gold_digital_divide AS

WITH state_reading AS (
    -- Step 1: Aggregate district-level NCES data → state level
    -- Weighted average: weight each district by its number of tested students
    SELECT
        fips,
        year,
        SUM(read_pct_prof_midpt * read_test_num_valid)
            / NULLIF(SUM(read_test_num_valid), 0)  AS reading_pct_proficient,
        SUM(math_pct_prof_midpt * read_test_num_valid)
            / NULLIF(SUM(read_test_num_valid), 0)  AS math_pct_proficient,
        SUM(read_test_num_valid)                   AS total_students_tested
    FROM silver_grade3_assessments
    WHERE all_students_flag = TRUE          -- "All Students" aggregate rows only
      AND read_pct_prof_midpt IS NOT NULL   -- exclude suppressed/missing scores
    GROUP BY fips, year
)

SELECT
    -- ── Identifiers ─────────────────────────────────────────────────────────
    r.fips,
    b.state_abbr,
    b.state_name,
    r.year,

    -- ── Outcome (Target Variable y) ─────────────────────────────────────────
    ROUND(r.reading_pct_proficient, 2)   AS reading_pct_proficient,
    ROUND(r.math_pct_proficient, 2)      AS math_pct_proficient,
    r.total_students_tested,

    -- ── Feature Set 1: Infrastructure Layer (FCC BDC) ───────────────────────
    ROUND(b.pct_25_3_mbps, 2)           AS broadband_pct_25_3,
    ROUND(b.pct_100_20_mbps, 2)         AS broadband_pct_100_20,

    -- ── Feature Set 2: Adoption Layer (Census HPS) ──────────────────────────
    ROUND(h.pct_internet_access, 2)     AS hps_pct_internet,
    ROUND(h.pct_computer_access, 2)     AS hps_pct_computer,
    ROUND(h.pct_ai_tool_use, 2)         AS hps_pct_ai_use,


    -- ── Engineered Feature 1: Connectivity tier (categorical) ────────────────
    -- Lecture talking point: categorical features require encoding for sklearn
    CASE
        WHEN b.pct_25_3_mbps >= 90.0 THEN 'high'
        WHEN b.pct_25_3_mbps >= 70.0 THEN 'medium'
        ELSE                               'low'
    END AS connectivity_tier,

    -- ── Engineered Feature 2: Infrastructure vs. adoption gap ────────────────
    -- High gap = state has broadband pipes but residents aren't using internet
    -- This signals a digital LITERACY problem, not an infrastructure problem
    ROUND(b.pct_25_3_mbps - h.pct_internet_access, 2) AS infra_adoption_gap,

    -- ── Engineered Feature 3: Proficiency gap vs. national weighted average ──
    -- Window function over all states in the same assessment year
    ROUND(
        r.reading_pct_proficient
        - AVG(r.reading_pct_proficient) OVER (PARTITION BY r.year),
        2
    ) AS proficiency_gap_vs_national

FROM state_reading r
JOIN silver_broadband b
    ON r.fips = CAST(b.state_fips AS INTEGER)
JOIN silver_ai_usage h
    ON r.fips = CAST(h.state_fips AS INTEGER);
