SELECT 
	grade AS grades_for_Alice_Johnson
FROM 
	grades
WHERE
	student_id IN (SELECT id FROM students WHERE full_name = 'Alice Johnson');


SELECT 
	students.full_name, AVG(grades.grade) AS avg_grade
FROM 
	students
JOIN 
	grades ON students.id = grades.student_id
GROUP BY 
	students.full_name;


SELECT
	full_name AS students_born_after_2004 FROM students
WHERE
	birth_year > 2004;


SELECT 
	DISTINCT subject AS list_of_subject, 
	AVG(grade) OVER(PARTITION BY subject)
FROM
	grades;


SELECT 
	students.full_name, AVG(grades.grade) AS avg_grade
FROM 
	students
JOIN 
	grades ON students.id = grades.student_id
GROUP BY 
	students.full_name
ORDER BY
	avg_grade DESC
LIMIT 3;


SELECT 
	DISTINCT full_name 
FROM 
	students
	WHERE id IN (SELECT student_id FROM grades WHERE grade > 80);