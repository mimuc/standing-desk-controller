PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    passwd TEXT,
    email TEXT,
    name TEXT NOT NULL,
    status INTEGER NOT NULL DEFAULT 1,
    standkey INTEGER NOT NULL DEFAULT 1,
    sitkey INTEGER NOT NULL DEFAULT 2,
    condition TEXT NOT NULL, -- can be R, A, or S (regular interval, apple watch, or smart)
    startdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- the date the user actually starts the experiment
);

DROP TABLE IF EXISTS desks;
CREATE TABLE desks (
    deskid INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    macaddress TEXT NOT NULL,
    location TEXT NOT NULL
);

DROP TABLE IF EXISTS heights;
CREATE TABLE heights (
    heightid INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    time INTEGER NOT NULL,
    userid INTEGER NOT NULL,
    height REAL NOT NULL
);

DROP TABLE IF EXISTS actions;
CREATE TABLE actions (
    actionid INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    time INTEGER NOT NULL,
    userid INTEGER NOT NULL,
    action TEXT NOT NULL -- manual keypresses, interface actions, and automatic actions
);

DROP TABLE IF EXISTS deskjoins;
CREATE TABLE deskjoins (
    deskjoinid INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end TIMESTAMP,
    deskid INTEGER NOT NULL,
    userid INTEGER NOT NULL
);

DROP TABLE IF EXISTS commands;
CREATE TABLE commands (
    commandid INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    userid INTEGER NOT NULL,
    command REAL NOT NULL, -- any of keys 1,2,3,4 or a specific height in cm to move to
    done INTEGER NOT NULL DEFAULT 0
    );