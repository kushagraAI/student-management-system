# RANK()
"""
SELECT user_id, RANK() OVER(PARTITION BY user_id ORDER BY COUNT(*) DESC) Rank
FROM twitch_sessions
WHERE session_type='viewer'
GROUP BY user_id;
"""


# DENSE_RANK()
"""
SELECT rc_users.company_id, rc_calls.user_id, DENSE_RANK() OVER(ORDER BY COUNT(*) DESC) Rank
FROM rc_calls
INNER JOIN rc_users
ON rc_calls.user_id = rc_users.user_id
GROUP BY rc_users.company_id, rc_calls.user_id;
ORDER BY COUNT(*) DESC;
"""


# ROW_NUMBER()
"""
SELECT *, second_last_rating.rating - avg_rating.rating  FROM
(SELECT name, rating
(SELECT *,
Row_number() OVER( partition BY nominee_filmography.name ORDER BY nominee_filmography.year DESC) AS row_number
FROM nominee_filmography) AS added_row_number
WHERE row_number=2) AS second_last_rating

RIGHT JOIN
(SELECT name, AVG(rating)
FROM nominee_filmography
GROUP BY name) AS avg_rating

ON avg_rating.name = second_last_rating.name;
"""
