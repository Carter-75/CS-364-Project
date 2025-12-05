-- Drop and recreate the database
DROP DATABASE IF EXISTS mediawatchlist;
CREATE DATABASE mediawatchlist;
USE mediawatchlist;

-- ==============================
-- TABLE CREATION
-- ==============================

-- Users table
CREATE TABLE User (
    UserId INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    ProfileName VARCHAR(50)
);

-- Genre table
CREATE TABLE Genre (
    GenreId INT AUTO_INCREMENT PRIMARY KEY,
    GenreName VARCHAR(50)
);

-- Platform table
CREATE TABLE Platform (
    PlatformId INT AUTO_INCREMENT PRIMARY KEY,
    PlatformName VARCHAR(50)
);

-- Media table
CREATE TABLE Media (
    MediaId INT AUTO_INCREMENT PRIMARY KEY,
    MediaName VARCHAR(100),
    MediaType VARCHAR(50),
    ReleaseYear INT,
    GenreId INT,
    PlatformId INT,
    Description TEXT,
    FOREIGN KEY (GenreId) REFERENCES Genre(GenreId),
    FOREIGN KEY (PlatformId) REFERENCES Platform(PlatformId)
);

-- Reviews table
CREATE TABLE Review (
    ReviewId INT AUTO_INCREMENT PRIMARY KEY,
    UserId INT,
    MediaId INT,
    Rating INT,
    ReviewText TEXT,
    Status ENUM ('Planning', 'Watching', 'Completed', 'Havent Watched') DEFAULT 'Planning',
    FOREIGN KEY (UserId) REFERENCES User(UserId),
    FOREIGN KEY (MediaId) REFERENCES Media(MediaId)
);

-- Watchlist table
CREATE TABLE Watchlist (
    UserId INT,
    MediaId INT,
    Status VARCHAR(20),
    PRIMARY KEY (UserId, MediaId),
    FOREIGN KEY (UserId) REFERENCES User(UserId),
    FOREIGN KEY (MediaId) REFERENCES Media(MediaId)
);

-- Link tables for many-to-many relationships
CREATE TABLE MediaGenre (
    MediaId INT,
    GenreId INT,
    FOREIGN KEY (MediaId) REFERENCES Media(MediaId),
    FOREIGN KEY (GenreId) REFERENCES Genre(GenreId)
);

CREATE TABLE MediaPlatform (
    MediaId INT,
    PlatformId INT,
    FOREIGN KEY (MediaId) REFERENCES Media(MediaId),
    FOREIGN KEY (PlatformId) REFERENCES Platform(PlatformId)
);

-- ==============================
-- CLEANUP (SAFE RESET)
-- ==============================

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE Watchlist;
TRUNCATE TABLE Review;
TRUNCATE TABLE Media;
TRUNCATE TABLE Platform;
TRUNCATE TABLE Genre;
TRUNCATE TABLE User;
SET FOREIGN_KEY_CHECKS = 1;

