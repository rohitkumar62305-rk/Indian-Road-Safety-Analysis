CREATE DATABASE road_safety_analytics;

USE road_safety_analytics;
USE road_safety_analytics;

CREATE TABLE road_accidents (
    sr_no INT,
    state_ut VARCHAR(100),
    road_accident_cases INT,
    road_accident_injured INT,
    road_accident_died INT,
    railway_accident_cases INT,
    railway_accident_injured INT,
    railway_accident_died INT,
    railway_crossing_cases INT,
    railway_crossing_injured INT,
    railway_crossing_died INT,
    total_accident_cases INT,
    total_accident_injured INT,
    total_accident_died INT
);
USE road_safety_analytics;

SELECT *
FROM road_accidents
LIMIT 10;

SELECT COUNT(*) AS total_records
FROM road_accidents;

SELECT
    state_ut,
    SUM(road_accident_cases) AS total_road_accidents,
    SUM(road_accident_injured) AS total_injured,
    SUM(road_accident_died) AS total_deaths
FROM road_accidents
GROUP BY state_ut
ORDER BY total_road_accidents DESC;

USE road_safety_analytics;

SELECT
    SUM(road_accident_cases) AS total_accidents,
    SUM(road_accident_injured) AS total_injured,
    SUM(road_accident_died) AS total_deaths
FROM road_accidents;

SELECT
    state_ut,
    SUM(road_accident_cases) AS total_accidents
FROM road_accidents
WHERE road_accident_cases IS NOT NULL
GROUP BY state_ut
ORDER BY total_accidents DESC
LIMIT 10;

USE road_safety_analytics;

-- 1. Total records in the dataset
SELECT COUNT(*) AS total_records
FROM road_accidents;


-- 2. Overall road accident statistics
SELECT
    SUM(road_accident_cases) AS total_road_accidents,
    SUM(road_accident_injured) AS total_injured,
    SUM(road_accident_died) AS total_deaths
FROM road_accidents;


-- 3. Location-wise road accident analysis
SELECT
    state_ut,
    SUM(road_accident_cases) AS total_accidents,
    SUM(road_accident_injured) AS total_injured,
    SUM(road_accident_died) AS total_deaths
FROM road_accidents
GROUP BY state_ut
ORDER BY total_accidents DESC;


-- 4. Top 10 locations by road accident cases
SELECT
    state_ut,
    SUM(road_accident_cases) AS total_accidents
FROM road_accidents
WHERE road_accident_cases IS NOT NULL
GROUP BY state_ut
ORDER BY total_accidents DESC
LIMIT 10;


-- 5. Top 10 locations by road accident deaths
SELECT
    state_ut,
    SUM(road_accident_died) AS total_deaths
FROM road_accidents
WHERE road_accident_died IS NOT NULL
GROUP BY state_ut
ORDER BY total_deaths DESC
LIMIT 10;


-- 6. Top 10 locations by road accident injuries
SELECT
    state_ut,
    SUM(road_accident_injured) AS total_injured
FROM road_accidents
WHERE road_accident_injured IS NOT NULL
GROUP BY state_ut
ORDER BY total_injured DESC
LIMIT 10;


-- 7. Railway accident analysis by location
SELECT
    state_ut,
    SUM(railway_accident_cases) AS railway_cases,
    SUM(railway_accident_injured) AS railway_injured,
    SUM(railway_accident_died) AS railway_deaths
FROM road_accidents
GROUP BY state_ut
ORDER BY railway_cases DESC;


-- 8. Railway crossing accident analysis
SELECT
    state_ut,
    SUM(railway_crossing_cases) AS crossing_cases,
    SUM(railway_crossing_injured) AS crossing_injured,
    SUM(railway_crossing_died) AS crossing_deaths
FROM road_accidents
GROUP BY state_ut
ORDER BY crossing_cases DESC;


-- 9. Locations with the highest total accident cases
SELECT
    state_ut,
    SUM(total_accident_cases) AS total_accident_cases,
    SUM(total_accident_injured) AS total_injured,
    SUM(total_accident_died) AS total_deaths
FROM road_accidents
GROUP BY state_ut
ORDER BY total_accident_cases DESC
LIMIT 10;


-- 10. Compare road, railway, and railway-crossing cases
SELECT
    SUM(road_accident_cases) AS road_cases,
    SUM(railway_accident_cases) AS railway_cases,
    SUM(railway_crossing_cases) AS railway_crossing_cases
FROM road_accidents;


-- 11. Locations with the highest death counts across accident categories
SELECT
    state_ut,
    SUM(road_accident_died) AS road_deaths,
    SUM(railway_accident_died) AS railway_deaths,
    SUM(railway_crossing_died) AS crossing_deaths
FROM road_accidents
GROUP BY state_ut
ORDER BY road_deaths DESC
LIMIT 10;


-- 12. Check for missing values in important columns
SELECT
    SUM(state_ut IS NULL OR state_ut = '') AS missing_location,
    SUM(road_accident_cases IS NULL) AS missing_road_cases,
    SUM(road_accident_injured IS NULL) AS missing_road_injuries,
    SUM(road_accident_died IS NULL) AS missing_road_deaths
FROM road_accidents;


-- 13. Check for duplicate location names
SELECT
    state_ut,
    COUNT(*) AS row_count
FROM road_accidents
GROUP BY state_ut
HAVING COUNT(*) > 1
ORDER BY row_count DESC;


-- 14. Calculate death-to-accident ratio by location
SELECT
    state_ut,
    SUM(road_accident_cases) AS total_accidents,
    SUM(road_accident_died) AS total_deaths,
    ROUND(
        100.0 * SUM(road_accident_died)
        / NULLIF(SUM(road_accident_cases), 0),
        2
    ) AS deaths_per_100_accidents
FROM road_accidents
GROUP BY state_ut
HAVING SUM(road_accident_cases) > 0
ORDER BY deaths_per_100_accidents DESC;


SELECT
    state_ut,
    SUM(road_accident_cases) AS total_accidents,
    SUM(road_accident_injured) AS total_injured,
    SUM(road_accident_died) AS total_deaths
FROM road_accidents
GROUP BY state_ut
ORDER BY total_accidents DESC
LIMIT 10;

SELECT
    COUNT(*) AS total_records,
    COUNT(state_ut) AS locations,
    SUM(road_accident_cases) AS road_accident_cases,
    SUM(road_accident_injured) AS total_injured,
    SUM(road_accident_died) AS total_deaths
FROM road_accidents;

SELECT *
FROM road_accidents;