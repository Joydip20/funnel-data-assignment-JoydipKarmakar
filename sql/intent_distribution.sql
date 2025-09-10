SELECT 
  COALESCE(NULLIF(TRIM(detected_intent),''),'unknown') AS intent,
  COUNT(*) AS cnt,
  ROUND(COUNT(*)*100.0 / (SELECT COUNT(*) FROM messages),2) AS pct_of_total
FROM messages
GROUP BY intent
ORDER BY cnt DESC;

SELECT m.detected_intent, COUNT(DISTINCT m.session_id) AS sessions_with_intent,
       COUNT(DISTINCT o.session_id) AS purchases_with_intent
FROM messages m
LEFT JOIN orders o ON m.session_id=o.session_id
GROUP BY m.detected_intent
ORDER BY purchases_with_intent DESC
LIMIT 2;
