CREATE TABLE passage (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    content TEXT,
    subject VARCHAR(255),
    question_count INT,
    topic VARCHAR(255)
);

CREATE TABLE question_and_explanation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    text TEXT,
    correct_answer VARCHAR(255),
    passage_id INT,
    explanations TEXT,
    FOREIGN KEY (passage_id) REFERENCES passage(id)
);

CREATE TABLE answer_choices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT,
    question_id INT,
    FOREIGN KEY (question_id) REFERENCES question_and_explanation(id)
);

