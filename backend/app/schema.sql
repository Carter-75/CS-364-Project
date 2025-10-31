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

-- ==============================
-- INSERT SAMPLE DATA
-- ==============================

-- 1
INSERT INTO User (FirstName, LastName, ProfileName)
VALUES ('Evan','Reed','BytePilot');
INSERT INTO Genre (GenreName)
VALUES ('Sci-Fi');
INSERT INTO Platform (PlatformName)
VALUES ('Netflix');
INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
VALUES ('Dune','Movie',2021,1,1,'Epic space adventure set on Arrakis');
INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
VALUES (1,1,5,'Visually stunning and deep','Completed');
INSERT INTO Watchlist (UserId, MediaId, Status)
VALUES (1,1,'Completed');

-- 2
INSERT INTO User (FirstName, LastName, ProfileName)
VALUES ('Ava','Kim','DataBloom');
INSERT INTO Genre (GenreName)
VALUES ('Pop');
INSERT INTO Platform (PlatformName)
VALUES ('Spotify');
INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
VALUES ('As It Was','Song',2022,2,2,'Emotional pop hit by Harry Styles');
INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
VALUES (2,2,4,'Catchy and nostalgic','Completed');
INSERT INTO Watchlist (UserId, MediaId, Status)
VALUES (2,2,'Completed');

-- 3
INSERT INTO User (FirstName, LastName, ProfileName)
VALUES ('Liam','Ross','NeoVision');
INSERT INTO Genre (GenreName)
VALUES ('Action');
INSERT INTO Platform (PlatformName)
VALUES ('HBO Max');
INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
VALUES ('The Batman','Movie',2022,3,3,'Dark gritty reboot of Gotham’s hero');
INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
VALUES (3,3,5,'Incredible cinematography','Completed');
INSERT INTO Watchlist (UserId, MediaId, Status)
VALUES (3,3,'Completed');

-- 4
INSERT INTO User (FirstName, LastName, ProfileName)
VALUES ('Olivia','Parker','CloudKnight');
INSERT INTO Genre (GenreName)
VALUES ('Comedy');
INSERT INTO Platform (PlatformName)
VALUES ('Netflix');
INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
VALUES ('The Good Place','Show',2016,4,4,'A hilarious take on the afterlife');
INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
VALUES (4,4,5,'Smart, funny, and heartwarming','Watching');
INSERT INTO Watchlist (UserId, MediaId, Status)
VALUES (4,4,'Watching');

-- 5
INSERT INTO User (FirstName, LastName, ProfileName)
VALUES ('Noah','Green','EchoStorm');
INSERT INTO Genre (GenreName)
VALUES ('Adventure');
INSERT INTO Platform (PlatformName)
VALUES ('Disney+');
INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
VALUES ('National Treasure','Movie',2004,5,5,'Historical mystery adventure film');
INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
VALUES (5,5,4,'Fun and nostalgic','Completed');
INSERT INTO Watchlist (UserId, MediaId, Status)
VALUES (5,5,'Completed');

-- 6
INSERT INTO User (FirstName, LastName, ProfileName)
VALUES ('Sophia','Carter','TechWhisper');
INSERT INTO Genre (GenreName)
VALUES ('Documentary');
INSERT INTO Platform (PlatformName)
VALUES ('YouTube');
INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
VALUES ('The Social Dilemma','Movie',2020,6,6,'Explores the dangers of social media');
INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
VALUES (6,6,5,'Eye-opening and essential','Completed');
INSERT INTO Watchlist (UserId, MediaId, Status)
VALUES (6,6,'Completed');

-- 7
INSERT INTO User (FirstName, LastName, ProfileName)
VALUES ('Mason','Lee','CyberDream');
INSERT INTO Genre (GenreName)
VALUES ('Thriller');
INSERT INTO Platform (PlatformName)
VALUES ('Hulu');
INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
VALUES ('Prey','Movie',2022,7,7,'A tense and clever Predator prequel');
INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
VALUES (7,7,4,'Great tension and storytelling','Watching');
INSERT INTO Watchlist (UserId, MediaId, Status)
VALUES (7,7,'Watching');

-- 8
INSERT INTO User (FirstName, LastName, ProfileName)
VALUES ('Isabella','Nguyen','CodeNova');
INSERT INTO Genre (GenreName)
VALUES ('Romance');
INSERT INTO Platform (PlatformName)
VALUES ('Netflix');
INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
VALUES ('To All The Boys I’ve Loved Before','Movie',2018,8,8,'Teen romantic comedy');
INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
VALUES (8,8,4,'Charming and heartfelt','Completed');
INSERT INTO Watchlist (UserId, MediaId, Status)
VALUES (8,8,'Completed');

-- 9
INSERT INTO User (FirstName, LastName, ProfileName)
VALUES ('Lucas','Adams','ByteForge');
INSERT INTO Genre (GenreName)
VALUES ('Horror');
INSERT INTO Platform (PlatformName)
VALUES ('Peacock');
INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
VALUES ('Five Nights at Freddy’s','Movie',2023,9,9,'Horror adaptation of the game');
INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
VALUES (9,9,3,'Creepy but predictable','Completed');
INSERT INTO Watchlist (UserId, MediaId, Status)
VALUES (9,9,'Completed');

-- 10
INSERT INTO User (FirstName, LastName, ProfileName)
VALUES ('Mia','Bennett','StarBlaze');
INSERT INTO Genre (GenreName)
VALUES ('Animation');
INSERT INTO Platform (PlatformName)
VALUES ('Disney+');
INSERT INTO Media (MediaName, MediaType, ReleaseYear, GenreId, PlatformId, Description)
VALUES ('Zootopia','Movie',2016,10,10,'Animated buddy-cop adventure');
INSERT INTO Review (UserId, MediaId, Rating, ReviewText, Status)
VALUES (10,10,5,'Creative and meaningful','Planning');
INSERT INTO Watchlist (UserId, MediaId, Status)
VALUES (10,10,'Planning');
