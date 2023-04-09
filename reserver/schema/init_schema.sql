DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    gender CHAR(1) NOT NULL,
    age INTEGER NOT NULL
);

DROP TABLE IF EXISTS admins;
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    email VARCHAR NOT NULL
);

DROP TABLE IF EXISTS venues;
CREATE TABLE venues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR UNIQUE NOT NULL,
    multiplier INTEGER NOT NULL DEFAULT 100, 
    capacity INTEGER NOT NULL,
    place VARCHAR NOT NULL,
    location VARCHAR NOT NULL
);

DROP TABLE IF EXISTS shows;
CREATE TABLE shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    rating INTEGER NOT NULL DEFAULT 0, 
    tags VARCHAR NOT NULL,
    price INTEGER NOT NULL,
    timing VARCHAR NOT NULL,
    venue_id INTEGER NOT NULL,
    booked_seats INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY(venue_id) REFERENCES venues(id) 
);

DROP TABLE IF EXISTS bookings;
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER NOT NULL,
    show_name VARCHAR NOT NULL,
    rating INTEGER, 
    user_id INTEGER NOT NULL,
    price INTEGER NOT NULL,
    booked_seats INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (show_id) REFERENCES shows (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);