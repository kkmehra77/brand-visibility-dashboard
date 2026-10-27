SELECT keyword, COUNT(*) AS total_products
FROM products
GROUP BY keyword
ORDER BY total_products DESC;

-- Q2: Overall average price
SELECT ROUND(AVG(price), 2) AS avg_price FROM products;

-- Q4: Overall average rating
SELECT ROUND(AVG(rating), 2) AS avg_rating FROM products;

-- Q5: Reviews ka distribution (low vs high engagement) - buckets me
SELECT
    CASE
        WHEN reviews < 100 THEN 'Low (0-100)'
        WHEN reviews < 1000 THEN 'Medium (100-1000)'
        ELSE 'High (1000+)'
    END AS engagement_level,
    COUNT(*) AS total
FROM products
GROUP BY engagement_level;
SELECT brand, COUNT(*) AS total
FROM products
GROUP BY brand
ORDER BY total DESC
LIMIT 5;
SELECT brand, ROUND(AVG(visibility_score), 4) AS avg_visibility
FROM products
GROUP BY brand
ORDER BY avg_visibility DESC
LIMIT 5;
SELECT brand, ROUND(AVG(position), 1) AS avg_position
FROM products
GROUP BY brand
ORDER BY avg_position ASC;
SELECT brand, COUNT(*) AS count_in_top10
FROM products
WHERE position <= 10
GROUP BY brand
ORDER BY count_in_top10 DESC;
SELECT brand, ROUND(AVG(rating), 2) AS avg_rating
FROM products
GROUP BY brand
ORDER BY avg_rating DESC
LIMIT 5;
SELECT price_range, COUNT(*) AS total
FROM products
GROUP BY price_range
ORDER BY total DESC;

SELECT platform, ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY platform
ORDER BY avg_price DESC;
SELECT keyword, title, price
FROM products p1
WHERE price = (
    SELECT MAX(price) FROM products p2 WHERE p2.keyword = p1.keyword
);

SELECT
    ROUND(SUM(CASE WHEN discount_pct > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
    AS pct_discounted
FROM products;
SELECT brand, ROUND(AVG(discount_pct), 2) AS avg_discount
FROM products
GROUP BY brand
ORDER BY avg_discount DESC
LIMIT 5;
SELECT platform, ROUND(AVG(discount_pct), 2) AS avg_discount
FROM products
GROUP BY platform
ORDER BY avg_discount DESC;
SELECT platform, COUNT(*) AS total_products
FROM products
GROUP BY platform
ORDER BY total_products DESC;
SELECT platform, ROUND(AVG(rating), 2) AS avg_rating
FROM products
GROUP BY platform
ORDER BY avg_rating DESC;
SELECT platform, ROUND(AVG(price), 2) AS avg_price
FROM products
GROUP BY platform
ORDER BY avg_price ASC;
SELECT platform, brand, COUNT(*) AS total
FROM products
GROUP BY platform, brand
ORDER BY platform, total DESC;
SELECT title, brand, visibility_score, position
FROM products
ORDER BY visibility_score DESC
LIMIT 10;
SELECT
    CASE WHEN position <= 10 THEN 'Top 10' ELSE 'Below 10' END AS rank_group,
    ROUND(AVG(reviews), 0) AS avg_reviews
FROM products
GROUP BY rank_group;
