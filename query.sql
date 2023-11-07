CREATE TABLE options (
    option_id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL
);

CREATE DATABASE freedb_quizmaster;

USE freedb_quizmaster;

SELECT * FROM user;

CREATE TABLE users (
    userid INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

select * from users;

USE quiz_master;

CREATE TABLE wdquiz_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct_option INT NOT NULL
);

CREATE DATABASE quiz_master;

select * from dmquiz_questions;
select * from dsnquiz_questions;
select * from ccquiz_questions;

CREATE TABLE quiz_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    score INT,
    quiz_date DATETIME,
    quiz_identifier VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(userid)
);

select * from quiz_results;
