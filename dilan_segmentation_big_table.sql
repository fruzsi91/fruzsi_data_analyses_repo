-- FULL QUERY

SELECT original_query.location,
       original_query.source,
       ROUND(AVG(reads_before_purchase.reads_before_purchase),2) AS avarage_reads_before_first_purchase,
       ROUND(AVG(reads_before_purchase.min_purchase_date - original_query.first_date),2) AS avarage_passday,
       SUM(original_query.user_purchase) as sum_revenue
FROM (SELECT first_read.my_date AS first_date,
             first_read.user_id,
             first_read.location,
             first_read.source,
             SUM(price) AS user_purchase
      FROM first_read
        JOIN purchases ON purchases.user_id = first_read.user_id
      GROUP BY first_read.user_id,
               first_read.location,
               first_read.source,
               first_read.my_date) AS original_query
  JOIN (SELECT user_id,
               TO_DATE(TO_CHAR(min_purchase,'yyyy-mm-dd'),'yyyy-mm-dd') AS min_purchase_date,
               COUNT(*) + 1 AS reads_before_purchase
        FROM (SELECT a.user_id,
                     a.date1,
                     MIN(b.date2) AS min_purchase
              FROM (SELECT user_id, my_date + my_time AS date1 FROM return_reads) AS a
                JOIN (SELECT user_id,
                             my_date + my_time AS date2
                      FROM purchases) AS b ON a.user_id = b.user_id
              GROUP BY a.user_id,
                       a.date1) AS c
        WHERE date1 <= min_purchase
        GROUP BY user_id,
                 min_purchase) AS reads_before_purchase ON original_query.user_id = reads_before_purchase.user_id
GROUP BY original_query.location,
         original_query.source
ORDER BY original_query.location,
         original_query.source;



