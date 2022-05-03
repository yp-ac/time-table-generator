from utils import *
from pathlib import Path
from collections import defaultdict
import json
from functools import lru_cache

class FacultyOverloadError(Exception):
    pass

@lru_cache(50)
def load_data(filename=Path('dummy-data.json')):
    with open(filename) as f:
        data = json.loads(f.read())

    courses = [Course(**c) for c in data['courses']]
    cd = {c.code: c for c in courses}
    for f in data['faculty']:
        f['courses'] = [cd[c] for c in f['courses']]
    instructor = [Instructor(**c) for c in data['faculty']]
    for f in data['departments']:
        f['courses'] = [cd[c] for c in f['courses']]
    dept = [Department(**c) for c in data['departments']]

    return courses, instructor, dept

def common_courses(departments):
    # (dept.num, course.name)
    # course -> dept.courses
    #        -> dept.number
    common_courses = defaultdict(lambda: set())

    for dept in departments: # co
        for dept_cmp in departments: # it
            if dept_cmp == dept: continue

            for course in dept.courses: # am2, pic, lb
                for course_cmp in dept_cmp.courses: # am1, pic, lb
                    if course == course_cmp: 
                        common_courses[course.code].add(dept.number)
                        common_courses[course.code].add( dept_cmp.number)

    return common_courses

def get_course(code):
    for course in courses:
        if course.code == code:
            return course
    return -1

def calculate_load(departments, instructors):
    load = defaultdict(lambda: 0)
    for dept in departments:
        for course in dept.courses:
            load[course.code] += len(dept.sections) * course.hours

    teachers = defaultdict(lambda: 0)
    for t in instructors:
        for course in t.courses:
            teachers[course.code] += 1

    assert len(load.keys()) == len(teachers.keys())

    for k in load.keys():
        load[k] /= teachers[k]

    load_per_teacher = defaultdict(lambda: 0)
    for t in instructors:
        for course in t.courses:
            load_per_teacher[t.name] += load[course.code]

    return load_per_teacher

def check_clash(time_tables, row, col, course):
    cnt = 0
    for tt in time_tables.values():
        # print(tt[row, col])
        if tt[int(row)][int(col)] == course: cnt += 1

    return cnt != 1

if __name__ == '__main__':
    courses, instructor, depts = load_data()
    load_faculty = calculate_load(depts, instructor)

    courses = {c.code : c for c in courses}
    # for k, v in load_faculty.items():
    #     if v > 22:
    #         raise FacultyOverloadError(f"{k} has too much work load!")

    common_course = common_courses(depts)

    time_tables = defaultdict(lambda: TimeTable())

    sort_var = {k: len(v) for k, v in common_course.items()}
    cc_sorted = sorted(common_course , key=sort_var.__getitem__, reverse=True)
    print(cc_sorted)    

    # O(n^5)
    # O(n^2)  worst case

    for c in cc_sorted:
        dept_ = common_course[c]
        for dept in depts:
            if dept.number not in dept_: continue

            for sec in dept.sections:
                for _ in range(courses[c].hours):
                    row, col = time_tables[sec].insert_random(c)
                    while check_clash(time_tables, row, col, c):
                        time_tables[sec][row, col] = None
                        row, col = time_tables[sec].insert_random(c)

                        if row == -1 or col == -1: raise IndexError("No More free lectures in the timetable")
            # break
    uncommon_courses = set(list(courses.keys())) - set(cc_sorted)
    print(uncommon_courses)
    for u in uncommon_courses:
        dept = list(filter(lambda dept: courses[u] in dept.courses, depts))[0]
        for sec in dept.sections:
            print(sec)
            for _ in range(courses[u].hours):
                row, col = time_tables[sec].insert_random(u)
                while check_clash(time_tables, row, col, u):
                    print(u, row, col)
                    time_tables[sec][row, col] = None
                    row, col = time_tables[sec].insert_random(u)

                    if row == -1 or col == -1: raise IndexError("No More free lectures in the timetable")
    for k, v in time_tables.items():
        print(k)
        print(v)
    # for r in range(5):
    #     for c in range(7):
    #         print(r, c, time_tables['N'][r][c])

    # print(time_tables['N'])
