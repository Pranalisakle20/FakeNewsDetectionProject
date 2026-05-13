-- Fake vs Real Count
SELECT news_type, COUNT(*)
FROM news_data
GROUP BY news_type;

-- Subject-wise Analysis
SELECT subject, COUNT(*) AS total_news
FROM news_data
GROUP BY subject
ORDER BY total_news DESC;

-- Fake News by Subject
SELECT subject, COUNT(*) AS fake_count
FROM news_data
WHERE news_type='Fake'
GROUP BY subject
ORDER BY fake_count DESC;

-- Monthly Trend
SELECT MONTH(date) AS month,
COUNT(*) AS total_news
FROM news_data
GROUP BY month
ORDER BY month;

-- Top 5 Categories
SELECT subject, COUNT(*) AS total
FROM news_data
GROUP BY subject
ORDER BY total DESC
LIMIT 5;