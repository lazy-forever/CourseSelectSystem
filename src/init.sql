-- 创建course数据库
DROP DATABASE IF EXISTS course;
CREATE DATABASE course;

-- 使用course数据库
USE course;

-- 创建students表
CREATE TABLE IF NOT EXISTS students (
  num INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (num)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 创建teachers表
CREATE TABLE IF NOT EXISTS teachers (
  num INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (num)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 创建course表
CREATE TABLE IF NOT EXISTS course (
  code VARCHAR(255) NOT NULL,
  name VARCHAR(255) DEFAULT NULL,
  credit VARCHAR(20) DEFAULT NULL,
  num INT NOT NULL,
  PRIMARY KEY (code),
  KEY tnum (num),
  CONSTRAINT tnum FOREIGN KEY (num) REFERENCES teachers (num) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 创建selects表
CREATE TABLE IF NOT EXISTS selects (
  num INT NOT NULL,
  code VARCHAR(255) NOT NULL,
  score FLOAT DEFAULT NULL,
  PRIMARY KEY (num, code),
  KEY code (code),
  CONSTRAINT code_fk FOREIGN KEY (code) REFERENCES course (code),
  CONSTRAINT snum_fk FOREIGN KEY (num) REFERENCES students (num)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- 向students表插入示例数据
INSERT INTO students (num, name, password) VALUES
(1, '张三', '123456'),
(2, '李四', 'abcdef'),
(3, '王五', 'qwerty');

-- 向teachers表插入示例数据
INSERT INTO teachers (num, name, password) VALUES
(101, '赵老师', 'teacher123'),
(102, '钱老师', 'pass123');

-- 向course表插入示例数据
INSERT INTO course (code, name, credit, num) VALUES
('CS101', '计算机基础', '3', 101),
('MATH201', '高等数学', '4', 102);

-- 向selects表插入示例数据
INSERT INTO selects (num, code, score) VALUES
(1, 'CS101', 85),
(2, 'MATH201', 78),
(3, 'CS101', 92),
(1, 'MATH201', 80);

DELIMITER //

CREATE TRIGGER before_student_insert
BEFORE INSERT ON students
FOR EACH ROW
BEGIN
  DECLARE msg VARCHAR(255);
  IF EXISTS (SELECT 1 FROM students WHERE num = NEW.num) THEN
    SET msg = CONCAT('Duplicate entry for num: ', NEW.num);
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
  END IF;
END;

//

DELIMITER ;