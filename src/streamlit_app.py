import hydralit as hy
from components import display_list_with_input_options
from collections import defaultdict
from algorithm import load_data, common_courses, check_clash
from utils import *

if 'COURSES' not in hy.session_state:
    courses, *_ = load_data()
    hy.session_state['COURSES'] = {c.code: c for c in courses}

if 'DEPARTMENTS' not in hy.session_state:
    *_, dept = load_data()
    hy.session_state['DEPARTMENTS'] = dept

if 'INSTRUCTORS' not in hy.session_state:
    _, faculty, _ = load_data()
    hy.session_state['INSTRUCTORS'] = faculty

INSTRUCTORS = hy.session_state.INSTRUCTORS
COURSES = hy.session_state.COURSES
DEPARTMENTS = hy.session_state.DEPARTMENTS

app = hy.HydraApp(title='Time Table Generator', favicon=":chart:", use_navbar=True, navbar_sticky=True)

@app.addapp(title="HOME", is_home=True)
def home():
    hy.header('Time Table Generator')
    hy.markdown('''
        This is a genuine project created by Yash Thakare ([@Yash24T](https://github.com/yash24t)) and Yash Pawar ([@yashppawar](https://github.com/yashppawar))
        
        The code for this project is available at [github.com/yp-ac/time-table-generator](https://github.com/yp-ac/time-table-generator)
    ''')


###### DEPARTMENTS PAGE ######
@app.addapp(title="Department")
def departments_page():
    def print_dept(dept: Department):
        def course_processor(out):
            if c := COURSES.get(out[0], None):
                dept.courses.append(c)
            else:
                hy.warning(f"{out[0]} does not exist!")

        with hy.expander(f"[{dept.number}] {dept.name}"):
            hy.write("Sections: ")

            display_list_with_input_options(
                dept.sections, 
                ['Section'],
                lambda out: dept.sections.append(out[0]),
                lambda x: hy.info(x),
                key=f"{dept.id}sp"
            )

            hy.write("Courses: ")

            display_list_with_input_options(
                dept.courses, 
                ['Course Code'],
                course_processor,
                lambda x: hy.info(f"[{x.code}] {x.name}"),
                key=f"{dept.id}cp"
            )

    display_list_with_input_options(
        DEPARTMENTS,
        ['Dept Name'],
        lambda out: DEPARTMENTS.append(Department(number=len(DEPARTMENTS), name=out[0])),
        print_dept,
        key='dp'
    )


###### Teachers PAGE ######
@app.addapp(title="Teachers")
def teachers():
    def teacher_to_str(teacher: Instructor):
        def teach_processor(out):
            if c := COURSES.get(out[0], None):
                teacher.courses.append(c)
            else:
                hy.warning(f"{out[0]} does not exist!")

        with hy.expander(teacher.name):
            hy.write("Courses: ")

            display_list_with_input_options(
                teacher.courses, 
                ["Course Code"],
                teach_processor, 
                lambda x: hy.info(f"[{x.code}] {x.name}"),
                key=teacher.id
            )

    display_list_with_input_options(
        INSTRUCTORS,
        ["Instructor Name"], 
        lambda out: INSTRUCTORS.append(Instructor(name=out[0])), 
        teacher_to_str, 
        key='ip'
    )

###### Courses PAGE ######
@app.addapp(title='Courses')
def courses_page():
    def processor(out):
        COURSES[out[0]] = Course(code=out[0], name=out[1], hours=int(out[2].strip()))

    def course_to_string(course: Course):
        return hy.info(f"[{course.code}] {course.name}")

    display_list_with_input_options(COURSES.values(), ["Course Code", "Course Name", "num hours"], processor, course_to_string, key='cp')


@app.addapp(title="Time Table")
def time_table_gen_page():
    hy.header("Time Table(s)")
    
    if hy.button("Generate Time Table"):
        common_course = common_courses(DEPARTMENTS)

        time_tables = defaultdict(lambda: TimeTable())

        sort_var = {k: len(v) for k, v in common_course.items()}
        cc_sorted = sorted(common_course , key=sort_var.__getitem__, reverse=True)
        print(cc_sorted)    

        for c in cc_sorted:
            dept_ = common_course[c]
            for dept in DEPARTMENTS:
                if dept.number not in dept_: continue

                for sec in dept.sections:
                    for _ in range(COURSES[c].hours):
                        row, col = time_tables[sec].insert_random(c)
                        while check_clash(time_tables, row, col, c):
                            time_tables[sec][row, col] = None
                            row, col = time_tables[sec].insert_random(c)

                            if row == -1 or col == -1: raise IndexError("No More free lectures in the timetable")

        uncommon_courses = set(list(COURSES.keys())) - set(cc_sorted)
        print(uncommon_courses)
        for u in uncommon_courses:
            dept = list(filter(lambda dept: COURSES[u] in dept.courses, DEPARTMENTS))[0]
            for sec in dept.sections:
                print(sec)
                for _ in range(COURSES[u].hours):
                    row, col = time_tables[sec].insert_random(u)
                    while check_clash(time_tables, row, col, u):
                        print(u, row, col)
                        time_tables[sec][row, col] = None
                        row, col = time_tables[sec].insert_random(u)

                        if row == -1 or col == -1: raise IndexError("No More free lectures in the timetable")

        def data_processor(data):
            if data is None: 
                return ''
            return COURSES[data].name

        for k, tt in time_tables.items():
            hy.write(f"Section: **{k}**")
            hy.table(tt.to_dataframe(data_processor))

if __name__ == '__main__':
    app.run()
