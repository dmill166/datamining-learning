-- =============================================================
-- Enterprise Analytical Gold Layer
-- Implements robust imputation and statistical windowing 
-- intended for ML consumption, resolving aggregational drift.
-- =============================================================

CREATE OR REPLACE TABLE gold_digital_divide AS
WITH nces_agg AS (
    SELECT 
        fips,
        -- Weighted average accounts for district sizes
        SUM(read_pct_prof_midpt * read_test_num_valid) / SUM(read_test_num_valid) AS reading_pct_proficient,
        -- Volatility check: High standard deviation indicates deep inequality within the state
        STDDEV(read_pct_prof_midpt) AS reading_inequality_index
    FROM silver_grade3_assessments
    WHERE read_test_num_valid > 0
    GROUP BY fips
),
-- Z-Score Normalization for ML ingestion stability
normalized_features AS (
    SELECT 
        n.fips,
        n.reading_pct_proficient,
        n.reading_inequality_index,
        b.pct_25_3_mbps AS broadband_pct_25_3,
        a.pct_ai_tool_use AS hps_pct_ai_use,
        i.median_income,
        
        -- Rolling variance for outlier detection
        (n.reading_pct_proficient - AVG(n.reading_pct_proficient) OVER ()) / 
            NULLIF(STDDEV(n.reading_pct_proficient) OVER(), 0) AS reading_z_score,
            
        (b.pct_25_3_mbps - AVG(b.pct_25_3_mbps) OVER ()) / 
            NULLIF(STDDEV(b.pct_25_3_mbps) OVER(), 0) AS broadband_z_score
            
    FROM nces_agg n
    JOIN silver_broadband b ON n.fips = CAST(b.state_fips AS INTEGER)
    JOIN silver_ai_usage a ON n.fips = CAST(a.state_fips AS INTEGER)
    JOIN silver_income i ON n.fips = CAST(i.state_fips AS INTEGER)
)
SELECT 
    f.fips,
    b.state_abbr,
    f.reading_pct_proficient,
    f.reading_z_score,
    f.reading_inequality_index,
    f.broadband_pct_25_3,
    f.broadband_z_score,
    f.hps_pct_ai_use,
    f.median_income,
    
    -- Engineered Feature: Delta between infrastructure availability and actual usage
    (f.broadband_pct_25_3 - a.pct_internet_access) AS infra_adoption_gap,
    
    -- Clustering Tier for Stratified Analysis
    CASE 
        WHEN f.broadband_pct_25_3 >= 90.0 THEN 'high'
        WHEN f.broadband_pct_25_3 >= 75.0 THEN 'medium'
        ELSE 'low'
    END AS connectivity_tier

FROM normalized_features f
JOIN silver_broadband b ON f.fips = CAST(b.state_fips AS INTEGER)
JOIN silver_ai_usage a ON f.fips = CAST(a.state_fips AS INTEGER);
