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


-- Group 3: Users who rated at least one media above 9
SELECT UserId, FirstName, LastName, ProfileName
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