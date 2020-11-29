class Reducer:
    def __init__(self, key, value):
        self.day_time_tuple = key
        self.value = value
        # Extract home_instructor, home_session, center_instructors
        self.home_instructor = None
        self.home_session = None
        self.center_instr_sess_tuples = []
        # session at 0, instructor at 1
        for item in value:
            if item[0].location == 'Home':
                self.home_session = item[0]
                self.home_instructor = item[1]
        for item in value:
            if item[0].location != 'Home':
                self.center_instr_sess_tuples.append(item)

    def reallocate_excess_center_capacity(self):
        if not self.home_session is None:
            replacement_capacity_required = self.home_instructor.max_sess_cnt - self.home_instructor.remaining_student_capacity(
                self.home_session)
            replacement_capacity_available = 0
            for i in self.center_instr_sess_tuples:
                replacement_capacity_available = replacement_capacity_available + i[1].remaining_student_capacity(i[0])
            if replacement_capacity_available >= replacement_capacity_required:
                self.home_session.remove_instructor(self.home_instructor)
                self.home_instructor.remove_session(self.home_session)
                for i in self.center_instr_sess_tuples: # todo step through this
                    if not self.home_session.fully_staffed():
                        self.home_session.add_duplex_instructor(i[1], i[1].sess_cnt[i[0]])
                        i[1].add_duplex_session(self.home_session, i[1].sess_cnt[i[0]])
            return self.home_session.fully_staffed()
        else:
            return False

