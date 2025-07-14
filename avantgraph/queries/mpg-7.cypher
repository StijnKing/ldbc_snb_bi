// 7. What are the top 10 most mentioned companies in messages, along with the number of mentions?
MATCH (m:Message::(c:Company))
WITH COUNT(*) AS mentions, c
RETURN c.name, mentions
ORDER BY mentions DESC
LIMIT 10;
