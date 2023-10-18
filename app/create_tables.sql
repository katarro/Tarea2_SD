CREATE TABLE regular_topic (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    phone VARCHAR(50),
    type VARCHAR(50),
    password VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE paid_topic (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    phone VARCHAR(50),
    type VARCHAR(50),
    password VARCHAR(255),
    email VARCHAR(255)
);