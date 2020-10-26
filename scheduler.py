import pygsheets
from instructor import Instructor
from duplexinstructor import DuplexInstructor
from session import Session
from reducer import Reducer

SHEET_WORK_AVAIL_NAME = 'Mathnasium Work Availability Form (Responses)'
INSTRUCTOR_SHEET_NAME = 'Form Responses 1'
SHEET_MASTER_NAME = 'Master Student Schedule (Version 6).20200910'
WKS_EXPECTED_STUDENTS_NAME = 'Expected Students'
WKS_ACTUAL_STUDENTS_NAME = 'Actual Students'

SHEET_INSTRUCTOR_SCHEDULE_NAME = 'Schedule.20201026'
WKS_SCHEDULE_NAME = 'Instructor Schedule'
ACT_STUDENT_COL_NUM = 7 # the column number of the previous weeks student counts

SECRET_FILE = 'C:\PythonPrograms\SchedulerGSheets\Working Directory\credentials.json'


def main():
    client = pygsheets.authorize(client_secret=SECRET_FILE)
    # create instructors
    instructors = Instructor.create_instructors(Instructor, client, SHEET_WORK_AVAIL_NAME,
                                                           INSTRUCTOR_SHEET_NAME)
    # instructors = DuplexInstructor.create_instructors(DuplexInstructor, client, SHEET_WORK_AVAIL_NAME,
    #                                                                    INSTRUCTOR_SHEET_NAME)
    # create required sessions
    sessions = Session.create_sessions(Session, client, SHEET_MASTER_NAME, WKS_ACTUAL_STUDENTS_NAME,ACT_STUDENT_COL_NUM)

    chancellor_sessions = []
    stafford_sessions = []
    home_sessions = []
    for s in sessions:
            if s.location == 'Chancellor':
                chancellor_sessions.append(s)
            elif s.location == 'Stafford':
                stafford_sessions.append(s)
            elif s.location == 'Home':
                home_sessions.append(s)

    # Pass 1. Assign instructors to serve at locations
    for l in [chancellor_sessions, stafford_sessions, home_sessions]:
        for s in l:
            for i in instructors:
                if not s.fully_staffed() and i.can_work_session(s):
                    i.add_session(s)
                    s.add_instructor(i)

    # Pass 2. Eliminate at home assignments where possible.
    # Find all instructors with unused capacity (serving 1 or 2 students)
    # Divide up into home instructors and center instructors
    # Eliminate at home assignments with in center capacity
    extra_capacity_session_instructor_tuples = Instructor.extra_capacity_session_instructor_tuples(Instructor, sessions)
    for key, value in extra_capacity_session_instructor_tuples.items(): Reducer(key, value).reallocate_excess_center_capacity()

    if True:
        print('Sessions Staffing Report')
        fully_staffed = []
        not_fully_staffed = []
        for s in sessions:
            if s.fully_staffed():
                fully_staffed.append(s)
            else:
                not_fully_staffed.append(s)
        print('--->Total Sessions:', len(sessions))
        print('------>Fully Staffed:', len(fully_staffed))
        print('------>Not Fully Staffed:', len(not_fully_staffed))
        for s in not_fully_staffed:
            s.print_pretty()

    if False:
        print('Staffing Efficiency Report\n')
        session_count = len(sessions)
        student_count = 0
        instructor_hours_count = 0
        for s in sessions:
            student_count = student_count + s.students_to_serve
        for i in instructors:
            instructor_hours_count = i.hours_scheduled() + instructor_hours_count
        students_per_instructor = student_count / instructor_hours_count

        print('Chancellor:', len(chancellor_sessions), 'Stafford:', len(stafford_sessions), 'Home:', len(home_sessions))
        print('Sessions provided:', session_count)
        print('Students served:', student_count)
        print("Instructor hours needed:", round(student_count / Instructor.max_sess_cnt))
        print('Instructor hours used:', instructor_hours_count)
        print('Ratio:', students_per_instructor)
        print('Waste: $', round((3 - students_per_instructor) * instructor_hours_count * 15))

    if False: #Print Instructor Schedules
        for i in instructors:
            i.print_schedule()
            print()

    if True: # Print Instructor Session Count
        print('Instructor Session Counts')
        for i in instructors:
            i.print_session_count()

    if True:
        print('Students Expected Each Session')
        for s in sessions:
            s.print()

    if True:
        Instructor.print_extra_capacity_instructors(Instructor, sessions)

    if False:
        Session.print_master_schedule(Session)

    if False: # print comma delimited sessions, by instructor, to transcript
        for i in instructors:
            i.print_sessions()

    if True:
        Instructor.write_sessions(Instructor, instructors, client, SHEET_INSTRUCTOR_SCHEDULE_NAME, WKS_SCHEDULE_NAME)

if __name__ == '__main__':
    main()
