from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(12), nullable=False, index=True)
    name = db.Column(db.String(12), index=True)
    password = db.Column(db.String(500), nullable=False, index=True)
    email = db.Column(db.String(26), index=True)
    phone = db.Column(db.String(26), index=True)
    sex = db.Column(db.String(26), index=True)
    birthday = db.Column(db.String(26), index=True)
    avatar = db.Column(db.String(62), index=True)
    role = db.Column(db.String(10), index=True)

    def to_json(self):
        json_data = {
            'user_id': self.user_id,
            'username': self.username,
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'phone': self.phone,
            'sex': self.sex,
            'birthday': self.birthday,
            'avatar': self.avatar,
            'role': self.role
        }
        return json_data


class Single(db.Model):
    __tablename__ = 'single'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(600), index=True)
    optionsA = db.Column(db.String(128), index=True)
    optionsB = db.Column(db.String(128), index=True)
    optionsC = db.Column(db.String(128), index=True)
    optionsD = db.Column(db.String(128), index=True)
    answer = db.Column(db.String(10), index=True)
    analysis = db.Column(db.String(64), index=True)
    degree = db.Column(db.String(10), index=True)
    course_id = db.Column(db.String(20), index=True)
    knowledge_point = db.Column(db.String(64), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'question': self.question,
            'optionsA': self.optionsA,
            'optionsB': self.optionsB,
            'optionsC': self.optionsC,
            'optionsD': self.optionsD,
            'answer': self.answer,
            'analysis': self.analysis,
            'degree': self.degree,
            'course_id': self.course_id,
            'knowledge_point': self.knowledge_point
        }
        return json_data


class Multiple(db.Model):
    __tablename__ = 'multiple'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(600), index=True)
    optionsA = db.Column(db.String(128), index=True)
    optionsB = db.Column(db.String(128), index=True)
    optionsC = db.Column(db.String(128), index=True)
    optionsD = db.Column(db.String(128), index=True)
    answer = db.Column(db.String(10), index=True)
    analysis = db.Column(db.String(64), index=True)
    degree = db.Column(db.String(10), index=True)
    course_id = db.Column(db.String(20), index=True)
    knowledge_point = db.Column(db.String(64), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'question': self.question,
            'optionsA': self.optionsA,
            'optionsB': self.optionsB,
            'optionsC': self.optionsC,
            'optionsD': self.optionsD,
            'answer': self.answer,
            'analysis': self.analysis,
            'degree': self.degree,
            'course_id': self.course_id,
            'knowledge_point': self.knowledge_point
        }
        return json_data


class Judgment(db.Model):
    __tablename__ = 'judgment'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(64), index=True)
    answer = db.Column(db.String(10), index=True)
    analysis = db.Column(db.String(64), index=True)
    degree = db.Column(db.String(10), index=True)
    course_id = db.Column(db.String(20), index=True)
    knowledge_point = db.Column(db.String(64), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'analysis': self.analysis,
            'degree': self.degree,
            'course_id': self.course_id,
            'knowledge_point': self.knowledge_point
        }
        return json_data


class Blank(db.Model):
    __tablename__ = 'blank'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(64), index=True)
    answer = db.Column(db.String(10), index=True)
    analysis = db.Column(db.String(64), index=True)
    degree = db.Column(db.String(10), index=True)
    course_id = db.Column(db.String(20), index=True)
    knowledge_point = db.Column(db.String(64), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'analysis': self.analysis,
            'degree': self.degree,
            'course_id': self.course_id,
            'knowledge_point': self.knowledge_point
        }
        return json_data


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(225), index=True)
    answer = db.Column(db.String(128), index=True)
    analysis = db.Column(db.String(64), index=True)
    degree = db.Column(db.String(10), index=True)
    course_id = db.Column(db.String(20), index=True)
    knowledge_point = db.Column(db.String(64), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'analysis': self.analysis,
            'degree': self.degree,
            'course_id': self.course_id,
            'knowledge_point': self.knowledge_point
        }
        return json_data


class Catalog(db.Model):
    __tablename__ = 'catalog'
    id = db.Column(db.String(64), primary_key=True)
    label = db.Column(db.String(64), unique=True, index=True)
    pid = db.Column(db.String(64), index=True)
    course_id = db.Column(db.String(20), index=True)
    isEdit = db.Column(db.String(5), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'label': self.label,
            'pid': self.pid,
            'course_id': self.course_id,
            'isEdit': int(self.isEdit)
        }
        return json_data


class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.String(64), primary_key=True)
    course_name = db.Column(db.String(64), unique=True, index=True)
    teacher_name = db.Column(db.String(64), index=True)

    def to_json(self):
        json_data = {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'teacher_name': self.teacher_name
        }
        return json_data


class ClassInfo(db.Model):
    __tablename__ = 'class_info'
    class_id = db.Column(db.Integer, primary_key=True, index=True)
    class_name = db.Column(db.String(10), unique=True, index=True)
    course_id = db.Column(db.String(10), index=True)
    class_code = db.Column(db.String(10), nullable=False, index=True)

    def to_json(self):
        json_data = {
            'class_id': self.class_id,
            'class_name': self.class_name,
            'course_id': self.course_id,
            'class_code': self.class_code
        }
        return json_data


class StudentClass(db.Model):
    __tablename__ = 'student_class'
    id = db.Column(db.Integer, index=True, primary_key=True)
    class_id = db.Column(db.String(10), nullable=False, index=True)
    student_id = db.Column(db.String(10), nullable=False, index=True)
    confirm = db.Column(db.String(10), nullable=False, index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'class_id': self.class_id,
            'student_id': self.student_id,
            'confirm': self.confirm
        }
        return json_data


class Paper(db.Model):
    __tablename__ = 'paper'
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.String(20), unique=True, index=True)
    paper_name = db.Column(db.String(10), unique=True, index=True)
    course_id = db.Column(db.String(20), index=True)
    knowledge_point = db.Column(db.String(20), index=True)
    paper_score = db.Column(db.String(10), index=True)
    paper_num = db.Column(db.String(10), index=True)
    single = db.Column(db.String(64), index=True)
    single_score = db.Column(db.String(10), index=True)
    multiple = db.Column(db.String(64), index=True)
    multiple_score = db.Column(db.String(10), index=True)
    judgment = db.Column(db.String(64), index=True)
    judgment_score = db.Column(db.String(10), index=True)
    blank = db.Column(db.String(64), index=True)
    blank_score = db.Column(db.String(10), index=True)
    answer = db.Column(db.String(64), index=True)
    answer_score = db.Column(db.String(10), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'paper_id': self.paper_id,
            'paper_name': self.paper_name,
            'course_id': self.course_id,
            'knowledge_point': self.knowledge_point,
            'paper_score': self.paper_score,
            'paper_num': self.paper_num,
            'single': self.single,
            'single_score': self.single_score,
            'multiple': self.multiple,
            'multiple_score': self.multiple_score,
            'judgment': self.judgment,
            'judgment_score': self.judgment_score,
            'blank': self.blank,
            'blank_score': self.blank_score,
            'answer': self.answer,
            'answer_score': self.answer_score
        }
        return json_data


class Exam(db.Model):
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.String(20), unique=True, index=True)
    exam_name = db.Column(db.String(10), unique=True, index=True)
    exam_course = db.Column(db.String(10), index=True)
    exam_class = db.Column(db.String(60), index=True)
    exam_type = db.Column(db.String(20), index=True)
    exam_score = db.Column(db.String(20), index=True)
    exam_date = db.Column(db.Date, index=True)
    start_time = db.Column(db.Time, index=True)
    end_time = db.Column(db.Time, index=True)
    answer_time = db.Column(db.String(20), index=True)
    attention = db.Column(db.String(128), index=True)
    exam_paper = db.Column(db.String(20), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'exam_id': self.exam_id,
            'exam_name': self.exam_name,
            'exam_course': self.exam_course,
            'exam_class': self.exam_class,
            'exam_type': self.exam_type,
            'exam_score': self.exam_score,
            'exam_date': self.exam_date.strftime('%Y-%m-%d'),
            'start_time': self.start_time.strftime('%H:%M:%S'),
            'end_time': self.end_time.strftime('%H:%M:%S'),
            'answer_time': self.answer_time,
            'attention': self.attention,
            'exam_paper': self.exam_paper
        }
        return json_data


class StudentResult(db.Model):
    __tablename__ = 'student_result'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.String(20), index=True)
    student_name = db.Column(db.String(20), index=True)
    score = db.Column(db.String(20), index=True)
    comment = db.Column(db.String(64), index=True)
    submissionTime = db.Column(db.String(64), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'exam_id': self.exam_id,
            'student_name': self.student_name,
            'score': self.score,
            'comment': self.comment,
            'submissionTime': self.submissionTime
        }
        return json_data


class ExamSingle(db.Model):
    __tablename__ = 'exam_single'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(20), index=True)
    exam_id = db.Column(db.String(20), index=True)
    single_id = db.Column(db.String(20), index=True)
    answer = db.Column(db.String(20), index=True)
    score = db.Column(db.String(5), index=True)
    status = db.Column(db.String(20), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'student_name': self.student_name,
            'exam_id': self.exam_id,
            'single_id': self.single_id,
            'answer': self.answer,
            'score': self.score,
            'status': self.status
        }
        return json_data


class ExamMultiple(db.Model):
    __tablename__ = 'exam_multiple'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(20), index=True)
    exam_id = db.Column(db.String(20), index=True)
    multiple_id = db.Column(db.String(20), index=True)
    answer = db.Column(db.String(20), index=True)
    score = db.Column(db.String(5), index=True)
    status = db.Column(db.String(20), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'student_name': self.student_name,
            'exam_id': self.exam_id,
            'multiple_id': self.multiple_id,
            'answer': self.answer,
            'score': self.score,
            'status': self.status
        }
        return json_data


class ExamJudgment(db.Model):
    __tablename__ = 'exam_judgment'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(20), index=True)
    exam_id = db.Column(db.String(20), index=True)
    judgment_id = db.Column(db.String(20), index=True)
    answer = db.Column(db.String(20), index=True)
    score = db.Column(db.String(5), index=True)
    status = db.Column(db.String(20), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'student_name': self.student_name,
            'exam_id': self.exam_id,
            'judgment_id': self.judgment_id,
            'answer': self.answer,
            'score': self.score,
            'status': self.status
        }
        return json_data


class ExamBlank(db.Model):
    __tablename__ = 'exam_blank'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(20), index=True)
    exam_id = db.Column(db.String(20), index=True)
    blank_id = db.Column(db.String(20), index=True)
    answer = db.Column(db.String(20), index=True)
    score = db.Column(db.String(20), index=True)
    status = db.Column(db.String(20), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'student_name': self.student_name,
            'exam_id': self.exam_id,
            'blank_id': self.blank_id,
            'answer': self.answer,
            'score': self.score,
            'status': self.status
        }
        return json_data


class ExamAnswer(db.Model):
    __tablename__ = 'exam_answer'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(20), index=True)
    exam_id = db.Column(db.String(20), index=True)
    answer_id = db.Column(db.String(20), index=True)
    answer = db.Column(db.String(128), index=True)
    score = db.Column(db.String(20), index=True)
    status = db.Column(db.String(20), index=True)

    def to_json(self):
        json_data = {
            'id': self.id,
            'student_name': self.student_name,
            'exam_id': self.exam_id,
            'answer_id': self.answer_id,
            'answer': self.answer,
            'score': self.score,
            'status': self.status
        }
        return json_data


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
