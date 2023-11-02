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

USE freedb_quizmaster;

CREATE TABLE pmquiz_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct_option INT NOT NULL
);

select * from dmquiz_questions;
select * from dsnquiz_questions;
select * from ccquiz_questions;


GRANT ALL PRIVILEGES ON quiz_master.* TO 'root'@'172.28.98.236';
CREATE USER IF NOT EXISTS 'root'@'172.28.98.236' IDENTIFIED BY 'Ademidun98!';
FLUSH PRIVILEGES;