-- =============================================================
-- eda_queries.sql
-- Supporting EDA queries run by EDAEngine (src/eda.py)
-- All queries assume gold_digital_divide has been materialized.
-- =============================================================

-- ── Query 1: Top 10 states by reading proficiency ──────────────────────────
-- Lecture demo: "Which states are winning and where do they sit on broadband?"
SELECT
    state_abbr,
    state_name,
    ROUND(reading_pct_proficient, 1)  AS reading_pct,
    ROUND(broadband_pct_25_3, 1)      AS broadband_pct,
    ROUND(hps_pct_ai_use, 1)          AS ai_use_pct,
    connectivity_tier
FROM gold_digital_divide
ORDER BY reading_pct_proficient DESC
LIMIT 10;

-- ── Query 2: Bottom 10 states by reading proficiency ──────────────────────
SELECT
    state_abbr,
    state_name,
    ROUND(reading_pct_proficient, 1)  AS reading_pct,
    ROUND(broadband_pct_25_3, 1)      AS broadband_pct,
    ROUND(hps_pct_ai_use, 1)          AS ai_use_pct,
    connectivity_tier
FROM gold_digital_divide
ORDER BY reading_pct_proficient ASC
LIMIT 10;

-- ── Query 3: Average proficiency by connectivity tier ─────────────────────
-- Lecture talking point: do tier categories predict the outcome variable?
SELECT
    connectivity_tier,
    COUNT(*)                                   AS state_count,
    ROUND(AVG(reading_pct_proficient), 2)      AS avg_reading_pct,
    ROUND(AVG(broadband_pct_25_3), 2)          AS avg_broadband_pct,
    ROUND(AVG(hps_pct_ai_use), 2)              AS avg_ai_use_pct
FROM gold_digital_divide
GROUP BY connectivity_tier
ORDER BY avg_reading_pct DESC;

-- ── Query 4: Pearson correlations (all features vs. reading proficiency) ───
-- Lecture talking point: correlation ≠ causation, but it identifies candidates
SELECT
    ROUND(CORR(broadband_pct_25_3, reading_pct_proficient), 4)   AS r_broadband_25_3,
    ROUND(CORR(broadband_pct_100_20, reading_pct_proficient), 4) AS r_broadband_100_20,
    ROUND(CORR(hps_pct_internet, reading_pct_proficient), 4)     AS r_internet_access,
    ROUND(CORR(hps_pct_computer, reading_pct_proficient), 4)     AS r_computer_access,
    ROUND(CORR(hps_pct_ai_use, reading_pct_proficient), 4)       AS r_ai_use,
    ROUND(CORR(infra_adoption_gap, reading_pct_proficient), 4)   AS r_infra_gap
FROM gold_digital_divide;

-- ── Query 5: Digital literacy gap states ──────────────────────────────────
-- States where broadband coverage is good but adoption lags significantly.
-- These states have an infrastructure investment that isn't translating to usage.
SELECT
    state_abbr,
    state_name,
    ROUND(broadband_pct_25_3, 1)    AS broadband_pct,
    ROUND(hps_pct_internet, 1)      AS internet_use_pct,
    ROUND(infra_adoption_gap, 1)    AS gap,
    ROUND(reading_pct_proficient, 1) AS reading_pct
FROM gold_digital_divide
WHERE infra_adoption_gap > 15
ORDER BY infra_adoption_gap DESC;

-- ── Query 6: Summary statistics for the Gold table ────────────────────────
SELECT
    COUNT(*)                                    AS total_states,
    ROUND(AVG(reading_pct_proficient), 2)       AS national_avg_reading,
    ROUND(MIN(reading_pct_proficient), 2)       AS min_reading,
    ROUND(MAX(reading_pct_proficient), 2)       AS max_reading,
    ROUND(AVG(broadband_pct_25_3), 2)           AS national_avg_broadband,
    ROUND(AVG(hps_pct_ai_use), 2)               AS national_avg_ai_use
FROM gold_digital_divide;
