CREATE SCHEMA cm;

CREATE TABLE cm.User (
    UserID SERIAL,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Gender gender_enum,
    Coin INT DEFAULT 1000,
    Login VARCHAR(50),
    Password TEXT
);

CREATE TABLE cm.Merch (
    MerchID SERIAL,
    Name VARCHAR(100),
    Coin INT,
    Count INT
);

CREATE TABLE cm.Storage (
    UserID INT,
    MerchID INT,
    Count INT
);

CREATE TABLE cm.Exchange (
    SenderID INT,
    RecipientID INT,
    Coin INT,
    Date TIMESTAMP
);