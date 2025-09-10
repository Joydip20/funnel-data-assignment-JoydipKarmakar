SELECT 
  COUNT(*) AS total_orders,
  SUM(canceled_at IS NOT NULL) AS canceled,
  SUM(TIMESTAMPDIFF(MINUTE, created_at, canceled_at) > 60) AS violations,
  ROUND(SUM(TIMESTAMPDIFF(MINUTE, created_at, canceled_at) > 60)*100.0 / SUM(canceled_at IS NOT NULL),2) AS violation_rate_pct
FROM orders;
