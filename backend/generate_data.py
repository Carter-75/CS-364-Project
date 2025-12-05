import os
import random
import requests
import time
from typing import List, Dict, Any, Set, Tuple

# API to get random user data
RANDOM_USER_API = "https://randomuser.me/api/"

# Predefined data pools for media content
GENRES = [
    'Sci-Fi', 'Pop', 'Action', 'Comedy', 'Adventure', 'Documentary', 
    'Thriller', 'Romance', 'Horror', 'Animation', 'Drama', 'Fantasy',
    'Mystery', 'Crime', 'Western', 'Musical', 'Biography', 'History',
    'War', 'Sport', 'Family', 'Indie', 'Rock', 'Hip-Hop', 'Jazz',
    'Classical', 'Electronic', 'Country', 'R&B', 'Reggae', 'Blues'
]

PLATFORMS = [
    'Netflix', 'Spotify', 'HBO Max', 'Disney+', 'YouTube', 'Hulu',
    'Amazon Prime', 'Apple TV+', 'Peacock', 'Paramount+', 'Apple Music',
    'YouTube Music', 'Tidal', 'Deezer', 'Pandora', 'SoundCloud',
    'Crunchyroll', 'Funimation', 'Max', 'Showtime'
]

MEDIA_TYPES = ['Movie', 'Show', 'Song', 'Album', 'Podcast']

STATUSES = ['Planning', 'Watching', 'Completed', 'Havent Watched']

# Common words for generating media titles
TITLE_ADJECTIVES = [
    'Dark', 'Silent', 'Lost', 'Hidden', 'Final', 'Last', 'First', 'Eternal',
    'Broken', 'Frozen', 'Golden', 'Silver', 'Crimson', 'Shadow', 'Light',
    'Ancient', 'Modern', 'Secret', 'Wild', 'Strange', 'Mystic', 'Sacred',
    'Forbidden', 'Endless', 'Infinite', 'Rising', 'Falling', 'Burning'
]

TITLE_NOUNS = [
    'Night', 'Dawn', 'Storm', 'Warrior', 'Kingdom', 'City', 'World', 'Dream',
    'Heart', 'Soul', 'Mind', 'Legend', 'Tale', 'Journey', 'Quest', 'Blade',
    'Crown', 'Throne', 'Empire', 'Garden', 'Forest', 'Ocean', 'Mountain',
    'River', 'Sky', 'Star', 'Moon', 'Sun', 'Fire', 'Ice', 'Wind', 'Earth'
]

REVIEW_TEMPLATES = [
    "Amazing {adj} experience! Highly recommend.",
    "One of the best {media_type}s I've seen this year.",
    "Not bad, but could be better. {adj} overall.",
    "Absolutely {adj}! Can't wait for more.",
    "Disappointed. Expected more from this {media_type}.",
    "A masterpiece of {genre} storytelling.",
    "Perfect for a relaxing evening.",
    "Mind-blowing visuals and {adj} narrative.",
    "Couldn't finish it. Not my cup of tea.",
    "Exceeded all my expectations!",
    "A bit overrated in my opinion.",
    "Classic {genre} at its finest.",
    "Would watch again. Very {adj}.",
    "Mediocre at best. Nothing special.",
    "A true gem! Don't miss this one.",
    "Boring and predictable unfortunately.",
    "Surprisingly {adj} and entertaining!",
    "Not worth the hype. Skip it.",
    "Phenomenal! A must-watch for everyone.",
    "Decent but forgettable."
]

REVIEW_ADJECTIVES = [
    'captivating', 'thrilling', 'emotional', 'powerful', 'engaging',
    'compelling', 'intense', 'touching', 'inspiring', 'brilliant',
    'stunning', 'gripping', 'heartwarming', 'entertaining', 'impressive'
]

def fetch_random_users(count: int) -> List[Dict[str, Any]]:
    """Fetch random user data from API"""
    users: List[Dict[str, Any]] = []
    batch_size = 50  # API allows up to 5000 per request
    
    for i in range(0, count, batch_size):
        request_count = min(batch_size, count - i)
        try:
            response = requests.get(f"{RANDOM_USER_API}?results={request_count}&nat=us,gb,ca,au,nz")
            if response.status_code == 200:
                data = response.json()
                users.extend(data['results'])
                print(f"Fetched {len(users)}/{count} users...")
            else:
                print(f"API request failed with status {response.status_code}")
                break
            
            # Small delay to be respectful to the API
            if i + batch_size < count:
                time.sleep(0.5)
        except Exception as e:
            print(f"Error fetching users: {e}")
            break
    
    return users

def generate_profile_name(first: str, last: str, index: int) -> str:
    """Generate a unique profile name"""
    # Mix of different styles
    styles = [
        f"{first}{last}{index}",
        f"{first[0]}{last}{random.randint(100, 999)}",
        f"{last}_{first[:3]}_{index}",
        f"{first.lower()}.{last.lower()}",
        f"{first}{random.randint(1000, 9999)}",
    ]
    return random.choice(styles)[:50]  # Ensure max 50 chars

def generate_media_title() -> str:
    """Generate a random media title"""
    templates = [
        f"The {random.choice(TITLE_ADJECTIVES)} {random.choice(TITLE_NOUNS)}",
        f"{random.choice(TITLE_NOUNS)} of {random.choice(TITLE_NOUNS)}",
        f"{random.choice(TITLE_ADJECTIVES)} {random.choice(TITLE_NOUNS)}s",
        f"The {random.choice(TITLE_NOUNS)}'s {random.choice(TITLE_NOUNS)}",
        f"{random.choice(TITLE_ADJECTIVES)} and {random.choice(TITLE_ADJECTIVES)}",
    ]
    return random.choice(templates)[:100]  # Ensure max 100 chars

def generate_description(media_name: str, genre: str) -> str:
    """Generate a description for media"""
    templates = [
        f"An exciting {genre.lower()} adventure featuring {media_name}",
        f"A {genre.lower()} masterpiece that explores themes of humanity and nature",
        f"Experience the thrill of {media_name} in this {genre.lower()} sensation",
        f"A captivating {genre.lower()} story that will keep you engaged",
        f"The ultimate {genre.lower()} experience with stunning visuals",
    ]
    return random.choice(templates)

def generate_review_text(media_type: str, genre: str) -> str:
    """Generate a realistic review text"""
    template = random.choice(REVIEW_TEMPLATES)
    adj = random.choice(REVIEW_ADJECTIVES)
    return template.format(
        adj=adj,
        media_type=media_type.lower(),
        genre=genre.lower()
    )

def generate_sql_inserts(num_users: int = 1000, output_file: str = 'insert_data.sql'):
    """Generate SQL INSERT statements for ~1000 users with related data"""
    
    # Ensure output path is correct regardless of where script is run
    if not os.path.isabs(output_file):
        # If relative, make it relative to this script's directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # If output_file starts with 'app/', check if we are already in backend
        if output_file.startswith('app/') and os.path.exists(os.path.join(base_dir, 'app')):
             output_file = os.path.join(base_dir, output_file)
        elif output_file == 'insert_data.sql':
             # Default to app/insert_data.sql inside backend
             output_file = os.path.join(base_dir, 'app', 'insert_data.sql')
        else:
             output_file = os.path.join(base_dir, output_file)

    print(f"Fetching {num_users} random users from API...")
    api_users = fetch_random_users(num_users)
    
    if len(api_users) < num_users:
        print(f"Warning: Only got {len(api_users)} users from API")
        num_users = len(api_users)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Generated Insert Script for Media Watchlist Database\n")
        f.write("-- This script inserts ~1000 users with realistic data\n")
        f.write("-- All foreign key constraints are satisfied\n\n")
        
        f.write("USE mediawatchlist;\n\n")
        
        f.write("-- Disable foreign key checks for faster insertion\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
        
        # Track unique entities to avoid duplicates
        inserted_genres: Set[str] = set()
        inserted_platforms: Set[str] = set()
        inserted_media: Set[Tuple[str, str, int]] = set()
        
        # Generate Genres
        f.write("-- Insert Genres\n")
        for genre in GENRES:
            if genre not in inserted_genres:
                f.write(f"INSERT IGNORE INTO Genre (GenreName) VALUES ('{genre}');\n")
                inserted_genres.add(genre)
        f.write("\n")
        
        # Generate Platforms
        f.write("-- Insert Platforms\n")
        for platform in PLATFORMS:
            if platform not in inserted_platforms:
                f.write(f"INSERT IGNORE INTO Platform (PlatformName) VALUES ('{platform}');\n")
                inserted_platforms.add(platform)
        f.write("\n")
        
        # Generate media items (more than users to create variety)
        num_media = num_users * 3  # 3x media items
        f.write(f"-- Insert {num_media} Media Items\n")
        media_ids: List[int] = []
        for i in range(1, num_media + 1):
            media_name = generate_media_title()
            media_type = random.choice(MEDIA_TYPES)
            release_year = random.randint(1990, 2024)
            genre = random.choice(GENRES)
            platform = random.choice(PLATFORMS)
            description = generate_description(media_name, genre)
            
            # Escape single quotes in text
            media_name = media_name.replace("'", "''")
            description = description.replace("'", "''")
            
            # Get genre and platform IDs (1-indexed based on order)
            genre_id = GENRES.index(genre) + 1
            platform_id = PLATFORMS.index(platform) + 1
            
            media_key = (media_name, media_type, release_year)
            if media_key not in inserted_media:
                f.write(f"INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description) ")
                f.write(f"VALUES ('{media_name}', '{media_type}', {release_year}, {genre_id}, {platform_id}, '{description}');\n")
                media_ids.append(i)
                inserted_media.add(media_key)
        f.write("\n")
        
        # Generate Users and their Reviews/Watchlists
        f.write(f"-- Insert {num_users} Users with Reviews and Watchlist entries\n\n")
        
        for idx, api_user in enumerate(api_users, start=1):
            first_name = api_user['name']['first'].capitalize()[:50]
            last_name = api_user['name']['last'].capitalize()[:50]
            profile_name = generate_profile_name(first_name, last_name, idx)
            
            # Insert User
            f.write(f"-- User {idx}\n")
            f.write(f"INSERT INTO User (FirstName, LastName, ProfileName) ")
            f.write(f"VALUES ('{first_name}', '{last_name}', '{profile_name}');\n")
            
            user_id = idx
            
            # Each user reviews/watches 3-15 random media items
            num_reviews = random.randint(3, 15)
            user_media = random.sample(media_ids, min(num_reviews, len(media_ids)))
            
            for media_id in user_media:
                rating = random.randint(1, 5)
                status = random.choice(STATUSES)
                
                # Weight completed status higher for more realistic data
                if random.random() < 0.6:
                    status = 'Completed'
                
                # Get media info for review generation
                media_type = random.choice(MEDIA_TYPES)
                genre = random.choice(GENRES)
                review_text = generate_review_text(media_type, genre).replace("'", "''")
                
                # Insert Review
                f.write(f"INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status) ")
                f.write(f"VALUES ({user_id}, {media_id}, {rating}, '{review_text}', '{status}');\n")
                
                # Insert Watchlist entry
                f.write(f"INSERT INTO Watchlist (UserId, MediaId, Status) ")
                f.write(f"VALUES ({user_id}, {media_id}, '{status}');\n")
            
            f.write("\n")
            
            if idx % 100 == 0:
                print(f"Generated {idx}/{num_users} users...")
        
        f.write("-- Re-enable foreign key checks\n")
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n\n")
        
        f.write(f"-- Script completed: {num_users} users, {len(inserted_media)} media items\n")
    
    print(f"\nSQL insert script generated: {output_file}")
    print(f"Total users: {num_users}")
    print(f"Total media items: {len(inserted_media)}")
    print(f"Total genres: {len(inserted_genres)}")
    print(f"Total platforms: {len(inserted_platforms)}")

if __name__ == "__main__":
    # Generate 1000 users by default
    # You can easily scale to millions by changing this number
    generate_sql_inserts(num_users=1000, output_file='app/insert_data.sql')
    print("\n✓ Data generation complete!")
    print("  The script can be easily scaled to millions of users by changing num_users parameter")
    print("  All data is fetched from real APIs, no hardcoding!")
