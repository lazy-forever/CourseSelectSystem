import pymysql

connection = pymysql.connect(host='mysql',
                             user='root',
                             password='password',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # 创建数据库
        cursor.execute("DROP DATABASE IF EXISTS course")
        cursor.execute("CREATE DATABASE course")
        cursor.execute("USE course")
        
        # 创建表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
              num INT NOT NULL,
              name VARCHAR(255) NOT NULL,
              password VARCHAR(255) NOT NULL,
              PRIMARY KEY (num)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
              num INT NOT NULL,
              name VARCHAR(255) NOT NULL,
              password VARCHAR(255) NOT NULL,
              PRIMARY KEY (num)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS course (
              code VARCHAR(255) NOT NULL,
              name VARCHAR(255) DEFAULT NULL,
              credit VARCHAR(20) DEFAULT NULL,
              num INT NOT NULL,
              PRIMARY KEY (code),
              KEY tnum (num),
              CONSTRAINT tnum FOREIGN KEY (num) REFERENCES teachers (num) ON DELETE RESTRICT ON UPDATE RESTRICT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS selects (
              num INT NOT NULL,
              code VARCHAR(255) NOT NULL,
              score FLOAT DEFAULT NULL,
              PRIMARY KEY (num, code),
              KEY code (code),
              CONSTRAINT code_fk FOREIGN KEY (code) REFERENCES course (code),
              CONSTRAINT snum_fk FOREIGN KEY (num) REFERENCES students (num)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
        """)
        
        # 插入示例数据
        cursor.executemany("""
            INSERT INTO students (num, name, password) VALUES (%s, %s, %s)
        """, [(1, '张三', '123456'), (2, '李四', 'abcdef'), (3, '王五', 'qwerty')])
        
        cursor.executemany("""
            INSERT INTO teachers (num, name, password) VALUES (%s, %s, %s)
        """, [(101, '赵老师', 'teacher123'), (102, '钱老师', 'pass123')])
        
        cursor.executemany("""
            INSERT INTO course (code, name, credit, num) VALUES (%s, %s, %s, %s)
        """, [('CS101', '计算机基础', '3', 101), ('MATH201', '高等数学', '4', 102)])
        
        cursor.executemany("""
            INSERT INTO selects (num, code, score) VALUES (%s, %s, %s)
        """, [(1, 'CS101', 85), (2, 'MATH201', 78), (3, 'CS101', 92), (1, 'MATH201', 80)])
        
    # 提交更改
    connection.commit()

finally:
    # 关闭游标和数据库连接
    connection.close()



def runSql(sql):
    conn = pymysql.connect(host='mysql', user='root', password='password', database='course', charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return result