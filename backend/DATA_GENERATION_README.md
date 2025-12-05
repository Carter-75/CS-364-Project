# Data Generation Script

This directory contains a Python script for generating realistic test data for the Media Watchlist database.

## Features

- **Real User Data**: Fetches actual names from the [RandomUser.me API](https://randomuser.me/)
- **Scalable**: Easily generate from 1,000 to millions of users
- **No Hardcoding**: All data is generated dynamically using external APIs and randomization
- **Complete Datasets**: Generates Users, Genres, Platforms, Media, Reviews, and Watchlist entries
- **Foreign Key Compliance**: All relationships and constraints are properly satisfied
- **Realistic Data**: 
  - Users have 3-15 media items each
  - 60% of entries have "Completed" status (realistic distribution)
  - Varied ratings (1-5 stars)
  - Context-aware review texts

## Generated Data Statistics

For the default 1000-user generation:
- **Users**: 1,000 unique users with real names
- **Media Items**: ~3,000 (3x the number of users)
- **Genres**: 31 diverse genres (Movies, TV, Music)
- **Platforms**: 20 streaming/media platforms
- **Reviews**: 6,000-15,000 (each user reviews 3-15 items)
- **Watchlist Entries**: Same as reviews

## Usage

### Basic Usage (1,000 users)

```bash
cd backend
python3 generate_data.py
```

This will generate `app/insert_data.sql` with 1,000 users.

### Scaling to More Users

To generate more users, modify the script or pass a parameter:

```python
# In generate_data.py, change the last line:
generate_sql_inserts(num_users=10000, output_file='app/insert_data.sql')
```

### Importing the Data

Once generated, import the SQL file into your database:

```bash
# Using MySQL command line
mysql -u your_username -p your_database < app/insert_data.sql

# Or using init_db.py (after modifying to include the insert script)
```

## Data Structure

### User Table
- **FirstName**: Real first names from API (max 50 chars)
- **LastName**: Real last names from API (max 50 chars)
- **ProfileName**: Unique generated usernames (max 50 chars)

### Media Table
- **MediaName**: Procedurally generated titles (max 100 chars)
- **MediaType**: Movie, Show, Song, Album, or Podcast
- **ReleaseYear**: Random years between 1990-2024
- **Description**: Context-aware descriptions

### Review Table
- **Rating**: 1-5 star ratings
- **ReviewText**: Contextual review text
- **Status**: Planning, Watching, Completed, or Havent Watched (60% Completed)

## Performance

- Generates 1,000 users in approximately 10-15 seconds
- API calls are batched (50 users per request)
- Respectful delays between API calls (0.5 seconds)
- SQL file size: ~2.7 MB for 1,000 users

## Scaling Considerations

For millions of users:

1. **Batch Processing**: Generate in chunks and merge SQL files
2. **Parallel API Calls**: Use async/await for faster API fetching
3. **Direct Database Insertion**: Consider using bulk INSERT instead of SQL files
4. **Database Optimization**: Use bulk loading utilities like `LOAD DATA INFILE`

### Example for 1 Million Users

```python
# Generate in batches
for batch in range(10):
    start = batch * 100000
    generate_sql_inserts(
        num_users=100000, 
        output_file=f'app/insert_data_batch_{batch}.sql'
    )
```

## Dependencies

- `requests`: For API calls
- `random`: For data generation (built-in)
- `time`: For API rate limiting (built-in)

Install dependencies:
```bash
pip install requests
```

## API Information

- **RandomUser.me API**: Free, no authentication required
- **Rate Limit**: Can request up to 5,000 users per call
- **Response Time**: ~200-500ms per request
- **Data Quality**: Real-looking names from multiple nationalities

## Customization

You can customize the following in `generate_data.py`:

- **GENRES**: Add/remove genre types
- **PLATFORMS**: Add/remove streaming platforms
- **MEDIA_TYPES**: Add/remove media types
- **REVIEW_TEMPLATES**: Add/remove review text patterns
- **num_reviews per user**: Change `random.randint(3, 15)` range
- **Completed status weight**: Adjust the 0.6 probability value

## File Output

The generated `app/insert_data.sql` includes:

1. Database selection statement
2. Foreign key checks disabled (for performance)
3. Genre insertions
4. Platform insertions
5. Media insertions (3,000 items)
6. User insertions with associated reviews and watchlist entries
7. Foreign key checks re-enabled
8. Summary comment with statistics

## Notes

- All text fields properly escape single quotes
- Uses `INSERT IGNORE` for genres/platforms to avoid duplicates
- Maintains referential integrity with proper foreign keys
- User IDs are sequential (1-1000)
- Media IDs are sequential (1-3000)

## Troubleshooting

**Issue**: API request fails
- **Solution**: Check internet connectivity, the API may be temporarily down

**Issue**: Duplicate key errors
- **Solution**: Ensure database is clean before importing, or use `INSERT IGNORE`

**Issue**: Foreign key constraint failures
- **Solution**: The script disables checks during insertion, ensure you run the complete script

**Issue**: Memory errors with large datasets
- **Solution**: Generate in smaller batches and import separately
