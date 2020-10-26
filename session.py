class Session:
    # class variables set by scheduler
    sessions = [] # all sessions instantiated by create_sessions
    students_per_instructor = 3
    time_dict = {'8:00 AM':'8 am', '9:00 AM' : '9 am', '10:00 AM': '10 am', '11:00 AM': '11 am', \
                '12:00 PM': '12 pm', '1:00 PM': '1 pm', '2:00 PM': '2 pm', '3:00 PM': '3 pm', \
                 '4:00 PM': '4 pm', '5:00 PM': '5 pm', '6:00 PM' : '6 pm', '7:00 PM' : '7 pm', \
                 '8:00 PM' : '8 pm'}
    day_dict = {'0':'Sunday', '1':'Monday', '2':'Tuesday', '3': 'Wednesday', '4':'Thursday', '5':'Friday', '6':'Saturday'}

    def __init__(self, data, student_count_col_num):
        self.day = data[0]
        self.location = data[1]
        self.time = self.time_dict[data[2]]
        self.students_to_serve = int(data[student_count_col_num]) # Actual Students column Number
        self.students_served = 0
        self.instructors = []
        self.day_time_tuple = [self.day,self.time]
        self.duplex_instructor = []

    def __lt__(self, other):
        return int(self.day) < int(other.day)

    def create_sessions(self, client, SHEET_MASTER_NAME, ACTUAL_STUDENTS_WKS_NAME, STUDENT_CNT_COL_NUM):
        master_schedule = client.open(SHEET_MASTER_NAME)
        sessions_wks = master_schedule.worksheet_by_title(ACTUAL_STUDENTS_WKS_NAME)
        for i in sessions_wks: self.sessions.append(Session(i,STUDENT_CNT_COL_NUM))
        self.sessions.pop(0)  # remove instance created from header
        # purge sessions with no students to serve
        sessions_with_students = []
        for s in self.sessions:
            if s.students_to_serve > 0:
                sessions_with_students.append(s)
        self.sessions = sessions_with_students
        return self.sessions

    def students_unserved(self):
        return self.students_to_serve - self.students_served

    def add_instructor(self, i, student_cnt = 0):
        self.instructors.append(i)
        i.sess_cnt[self] = student_cnt
        if self.students_unserved() >= i.student_capacity(self):
            # take all the capacity
            self.students_served = self.students_served + i.student_capacity(self)
            i.sess_cnt[self] = i.sess_cnt[self] + i.student_capacity(self)
        else:
            # take what is needed (should be 1 or 2)
            need = self.students_unserved()
            self.students_served = self.students_served + need
            i.sess_cnt[self] = i.sess_cnt[self] + need

    def add_duplex_instructor(self, i, student_cnt):
            self.add_instructor(i, student_cnt)
            self.duplex_instructor.append(i)

    # for use by reducer only
    def remove_instructor(self, outgoing):
        self.students_served = self.students_served - outgoing.sess_cnt[self]
        self.instructors.remove(outgoing)

    # for use by reducer only
    def replace_instructor(self, outgoing, replacement):
        self.remove_instructor(self, outgoing)
        self.add_instructor(replacement)

    def fully_staffed(self):
#        print('Serving: '+str(self.students_served)+ ' To serve: ' + str(self.students_to_serve))
        return self.students_served >= self.students_to_serve

    def print(self):
        print('Fully Staffed:', self.fully_staffed(), 'Day:', self.day, 'Loc:', self.location, 'Time:', self.time, 'Students:', self.students_to_serve, 'Instructors:', len(self.instructors))

    def print_pretty(self):
        print('--------->', self.day_dict[self.day], self.location, self.time, 'Underserved students: ', str(self.students_to_serve - self.students_served))

    def print_master_schedule(self):
        print('Total Sessions:', len(self.sessions))
        for s in self.sessions:
            print('Master Schedule for ' + s.day_dict[s.day] + ' ' + s.time + ' ' + s.location)

    def scheduled_session_times(self):
        scheduled_session_times = []
        for s in self.sessions:
            scheduled_session_times.append(s.time)
        #order times
        return list(set(scheduled_session_times))

    def scheduled_session_days(self):
        scheduled_session_days = []
        for s in self.sessions:
            scheduled_session_days.append(s.time)
        return list(set(scheduled_session_days))

    def comma_delimited_scheduled_session_times(self):
        result = ''
        times = self.scheduled_session_times(self)
        for t in times:
            if not t == times[len(times) - 1]:
                result = result + t + ','
            else:
                result = result + t
        print('10 am,11 am,12 pm,4 pm,3 pm,4 pm,5 pm,6 pm')
        result = '10 am,11 am,12 pm,4 pm,3 pm,4 pm,5 pm,6 pm'
        return result

    def session_record(self):
        return [self.day_dict[self.day], self.time, self.location]










