from collections import defaultdict
import os
from prettytable import PrettyTable
import sqlite3


class Student:

    def __init__(self, p_info, major_info):
        if len(p_info) == 2 or any([item.isspace() for item in p_info]) or '' in p_info:
            raise ValueError("Missing basic information of students!")

        self.CWID, self.name, self.major = p_info
        self.major_info = major_info
        self.courses = defaultdict(int)

    def add_stu_course(self, course, grade):
        self.courses[course] = grade

    def get_whole_info(self):
        """ return whole info of students including grades """
        return [self.CWID, self.name, self.major, self.courses]

    def pr_student(self):
        if not self.courses.items():
            return [self.CWID, self.name, self.major, None, None]
        else:
            return [self.CWID, self.name, self.major, sorted(list(self.courses.keys()))]


class Instructor:

    def __init__(self, p_info):
        if len(p_info) == 2 or any([item.isspace() for item in p_info]) or '' in p_info:
            raise ValueError("Missing basic information of instructors!")

        self.CWID, self.name, self.department = p_info
        self.courses = defaultdict(int)

    def add_ins_course(self, course):

        self.courses[course] += 1

    def get_whole_info(self):
        """ return whole info of instructors """
        return [self.CWID, self.name, self.department, self.courses]

    def pr_instructor(self):

        for course, count in self.courses.items():
            yield [self.CWID, self.name, self.department, course, count]

class Major:
    def __init__(self, major):
        self.major = major
        self.required = set()
        self.elective = set()

    def update_major(self, flag, course):
        if flag == 'R':
            self.required.add(course)
        elif flag == 'E':
            self.elective.add(course)
        else:
            raise ValueError("Error! Unknown course flag!")

    def get_major_info(self):
        return [self.major, sorted(list(self.required)), sorted(list(self.elective))]

    def update_courses_info(self, courses):
        passed_grades = ('A', 'A-', 'B+', 'B', 'B-', 'C+', 'C')  # the grades needed to pass the course
        completed_courses = set()
        for course, grade in courses.items():
            if grade == ' ':  # in case there is no grade for the course yet
                continue
            elif grade in passed_grades:
                completed_courses.add(course)

        remaining_required = self.left_required(completed_courses)
        remaining_electives = self.left_electives(completed_courses)

        return [sorted(list(completed_courses)), remaining_required, remaining_electives]

    def left_required(self, courses):
        if self.required.difference(courses) == set():  # no required course left
            return None
        else:
            return sorted(list(self.required.difference(courses)))

    def left_electives(self, courses):
        left_courses = self.elective.difference(courses)
        if len(left_courses) < len(self.elective):  # at least one elective course is needed
            return None
        else:  # no elective courses has been completed
            return sorted(list(self.elective))

    def get_whole_info(self):
        return [self.major, self.required, self.elective]


class Repository:

    def __init__(self, dir_path):

        self.students_path = os.path.join(dir_path, 'students.txt')
        self.instructors_path = os.path.join(dir_path, 'instructors.txt')
        self.grades_path = os.path.join(dir_path, 'grades.txt')
        self.majors_path = os.path.join(dir_path, 'majors.txt')
        try:
            os.chdir(dir_path)
        except FileNotFoundError:
            raise NotADirectoryError("Please provide a valid directory")

        self.students = dict()
        self.instructors = dict()
        self.majors = dict()
        self.majors_pth()
        self.students_pth()
        self.instructors_pth()
        self.grades_pth()

        self.print_student_table()
        self.print_instructor_table()
        self.print_major_table()

    def file_reader(self, file_path, delimeter):

        try:
            file = open(file_path, 'r')
            lines = file.readlines()[1:]
            file.close()
        except FileNotFoundError as e:
            print('Error! Cannot open file {}'.format(file_path))
        else:
            for line in lines:
                yield line.strip().split(delimeter)
        
    def students_pth(self):

        for p_info in self.file_reader(self.students_path, '\t'):
            CWID, name, major = p_info

            if major not in self.majors:
                raise ValueError('Error! Missing major {} information.'.format(major))

            if CWID not in self.students:
                self.students[CWID] = Student(p_info, self.majors[major])

    def instructors_pth(self):

        for p_info in self.file_reader(self.instructors_path, '\t'):
            self.instructors[p_info[0]] = Instructor(p_info)

    def grades_pth(self):

        for CWID_stu, course, grade, CWID_ins in self.file_reader(self.grades_path, '\t'):
            if CWID_stu not in self.students.keys():
                raise ValueError('Student CWID {} is not in the student system.'.format(CWID_stu))

            if CWID_ins not in self.instructors.keys():
                raise ValueError('Instructor CWID {} is not in the instructor system.'.format(CWID_stu))

            self.students[CWID_stu].add_stu_course(course, grade)
            self.instructors[CWID_ins].add_ins_course(course)

    def majors_pth(self):
        for major, flag, course in self.file_reader(self.majors_path, '\t'):
            if major not in self.majors:
                self.majors[major] = Major(major)

            self.majors[major].update_major(flag, course)

    def print_student_table(self):

        pt = PrettyTable(
            field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        for person in self.students.values():
            courses = self.majors[person.major].update_courses_info(person.courses)

            CWID, name, major, c = person.pr_student()
            p_info = [CWID, name, major]  # ignore the courses info
            for item in courses:
                p_info.append(item)

            pt.add_row(p_info)
        print(pt)
        return(pt)

    def print_instructor_table(self):

        pt = PrettyTable(field_names=['CWID', 'Name', 'Department', 'Courses', 'Student Num'])
        for person in self.instructors.values():
            for c in person.pr_instructor():
                pt.add_row(c)
        print(pt)
        return(pt)

    def print_major_table(self):
        pt = PrettyTable(field_names=['Major', 'Required Courses', 'Electives'])
        for major in self.majors.values():
            pt.add_row(major.get_major_info())
        print(pt)
        return(pt)

    def instructor_table_db(self, db_path):
        """ Print the instructor data in a pretty table """
        l = []
        db = sqlite3.connect(db_path)
        query = "select Ins.CWID, Ins.Name , Ins.Dept, Gra.Course, count(*) as Students from instructors Ins join grades Gra  on Ins.CWID = Gra.InstructorCWID GROUP BY Gra.InstructorCWID,Gra.Course order by  CWID desc;"
        pt = PrettyTable(field_names = ['CWID', 'Name', 'Dept', 'Course', 'Student'])
        for row  in db.execute(query):
            pt.add_row(list(row))
            l.append(row)
        print(pt)
        return(l)


def main():
    dir_path = 'C:\Stevens\Fall2019\SSW-810\Stevens'
    stevens = Repository(dir_path)
    stevens.instructor_table_db(db_path = '810_startup.db')

    


if __name__ == '__main__':
    main()
