-- Group 1: Top 5 highest-rated media overall by type
SELECT 
    Media.MediaType,
    Media.MediaName,
    ROUND(AVG(Review.Rating), 2) AS AvgRating
FROM Review
JOIN Media ON Review.MediaId = Media.MediaId
GROUP BY Media.MediaId, Media.MediaType
ORDER BY AvgRating DESC
LIMIT 5;

-- Group 2: Top 5 users who completed the most media (at least 5 completions)
SELECT 
    u.FirstName, 
    u.LastName, 
    COUNT(*) AS media_done
FROM User AS u
JOIN Review AS r ON u.UserId = r.UserId
WHERE r.Status = 'Completed'
GROUP BY u.UserId, u.FirstName, u.LastName
HAVING media_done > 5
ORDER BY media_done DESC
LIMIT 5 OFFSET 0;

-- Group 2: Top 5 media with the most completions (at least 5 completions)
SELECT 
    m.MediaName, 
    COUNT(*) AS user_completions
FROM Media AS m
JOIN Review AS r ON m.MediaId = r.MediaId
WHERE r.Status = 'Completed'
GROUP BY m.MediaId, m.MediaName
HAVING user_completions > 5
ORDER BY user_completions DESC
LIMIT 5 OFFSET 0;

-- Group 2: Average rating per genre
SELECT 
    AVG(r.Rating) AS avg_rating, 
    g.GenreName
FROM Review AS r
JOIN Media AS m ON r.MediaId = m.MediaId
JOIN Genre AS g ON m.GenreId = g.GenreId
GROUP BY g.GenreName;

-- Group 3: Users who rated at least one media above 9
SELECT 
    UserId, 
    FirstName, 
    LastName, 
    ProfileName
FROM User
WHERE UserId IN (
    SELECT UserId
    FROM Review
    WHERE Rating >= 4
);

-- Group 3: 10 most recent low-rated media (rating ≤ 3)
SELECT 
    Media.MediaName,
    Media.MediaType,
    Media.ReleaseYear,
    Review.Rating
FROM Review
JOIN Media ON Review.MediaId = Media.MediaId
WHERE Review.Rating <= 3
ORDER BY Media.ReleaseYear DESC
LIMIT 10;
