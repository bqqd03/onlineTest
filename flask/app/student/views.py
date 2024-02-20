import datetime
import random

from flask import request, jsonify

from . import student
from .. import db
from ..models import Course, User, Single, Multiple, Judgment, Blank, Answer, Paper, StudentClass, ClassInfo, Exam, \
    StudentResult, ExamSingle, ExamMultiple, ExamBlank, ExamJudgment, ExamAnswer


@student.route('/get_class', methods=['POST'])
def get_courses():
    user_id = request.json.get('user_id')
    user_class = StudentClass.query.filter_by(student_id=user_id, confirm='1').all()
    data = []
    for i in user_class:
        class_data = ClassInfo.query.filter_by(class_code=i.class_id).first()
        data.append(class_data.to_json())

    for h in data:
        course_name = Course.query.filter_by(course_id=h['course_id']).first()
        h['course_name'] = course_name.course_name
    return jsonify(data)


@student.route('/apply_class', methods=['POST'])
def apply_class():
    class_code = request.json.get('classCode')
    user_id = request.json.get('user_id')
    class_data = ClassInfo.query.filter_by(class_code=class_code).first()
    if class_data is None:
        return jsonify({'code': 400, 'message': '没有该班级码'})
    else:
        class_stu = StudentClass(class_id=class_code,
                                 student_id=user_id,
                                 confirm='0')
        db.session.add(class_stu)
        db.session.commit()
        return jsonify({'code': 200})


@student.route('/get_exam', methods=['POST'])
def get_exam():
    username = request.json.get('username')
    user_data = User.query.filter_by(username=username).first()
    class_data = StudentClass.query.filter_by(student_id=user_data.user_id).all()

    current_datetime = datetime.datetime.now()
    dayDate = datetime.date.today()
    current_time = current_datetime.time()
    datas = []

    for i in class_data:
        exam_data = Exam.query.filter_by(exam_class=i.class_id).all()
        for j in exam_data:
            data = j.to_json()
            course = Course.query.filter_by(course_id=j.exam_course).first()
            data['course_name'] = course.course_name

            if dayDate > j.exam_date:
                data['situation'] = '已结束'
            elif dayDate == j.exam_date:
                if current_time < j.start_time:
                    data['situation'] = '未开始'
                elif j.start_time <= current_time <= j.end_time:
                    data['situation'] = '进行中'
                elif current_time > j.end_time:
                    data['situation'] = '已结束'
            elif dayDate < j.exam_date:
                data['situation'] = '未开始'

            result_data = StudentResult.query.filter_by(student_name=username, exam_id=j.exam_id).first()
            if result_data is not None:
                data['situation'] = '已考完'
                data['score'] = result_data.score
            datas.append(data)

    return jsonify(datas)


@student.route('/exam_paper', methods=['POST'])
def exam_paper():
    exam_id = request.json.get('exam_id')
    exam_data = Exam.query.filter_by(exam_id=exam_id).first()
    datas = {}
    paper_data = Paper.query.filter_by(paper_id=exam_data.exam_paper).first()
    question_id = {'单选题': paper_data.single.split(','), '多选题': paper_data.multiple.split(','),
                   '判断题': paper_data.judgment.split(','), '填空题': paper_data.blank.split(','),
                   '问答题': paper_data.answer.split(',')}
    question_score = {'单选题': paper_data.single_score, '多选题': paper_data.multiple_score,
                      '判断题': paper_data.judgment_score, '填空题': paper_data.blank_score,
                      '问答题': paper_data.answer_score}

    data_classes = {
        '单选题': Single,
        '多选题': Multiple,
        '判断题': Judgment,
        '填空题': Blank,
        '问答题': Answer
    }
    for item in data_classes:
        data = []
        for i in question_id[item]:
            question_data = data_classes[item].query.filter_by(id=i).first()
            if question_data is not None:
                question = question_data.to_json()
                question['score'] = question_score[item]
                question['studentAnswer'] = ''
                if item == '多选题':
                    question['answers'] = question['answer'].split(',')
                    question['studentAnswer'] = []

                data.append(question)
        datas[item] = data
    return jsonify({'examData': exam_data.to_json(), 'paperData': datas})


@student.route('/save_exam', methods=['POST'])
def save_exam():
    question = request.json.get('question')
    examData = request.json.get('examData')
    score = 0
    for single in question['single']:
        if single['answer'] == single['studentAnswer']:
            score += int(single['score'])
            single['status'] = 'success'
        else:
            single['status'] = 'error'
        exam_single = ExamSingle(student_name=examData['student_name'],
                                 exam_id=examData['exam_id'],
                                 single_id=single['id'],
                                 answer=single['studentAnswer'],
                                 score=single['score'],
                                 status=single['status'])
        db.session.add(exam_single)

    for multiple in question['multiple']:
        if sorted(multiple['answers']) == sorted(multiple['studentAnswer']):
            score += int(multiple['score'])
            multiple['status'] = 'success'
        else:
            multiple['status'] = 'error'
        exam_multiple = ExamMultiple(student_name=examData['student_name'],
                                     exam_id=examData['exam_id'],
                                     multiple_id=multiple['id'],
                                     answer=','.join(multiple['studentAnswer']),
                                     score=multiple['score'],
                                     status=multiple['status'])
        db.session.add(exam_multiple)

    for judgment in question['judgment']:
        if judgment['answer'] == judgment['studentAnswer']:
            score += int(judgment['score'])
            judgment['status'] = 'success'
        else:
            judgment['status'] = 'error'
        exam_judgment = ExamJudgment(student_name=examData['student_name'],
                                     exam_id=examData['exam_id'],
                                     judgment_id=judgment['id'],
                                     answer=judgment['studentAnswer'],
                                     score=judgment['score'],
                                     status=judgment['status'])
        db.session.add(exam_judgment)

    for blank in question['blank']:
        if blank['answer'] == blank['studentAnswer']:
            score += int(blank['score'])
            blank['status'] = 'success'
        else:
            blank['status'] = 'error'
        exam_blank = ExamBlank(student_name=examData['student_name'],
                               exam_id=examData['exam_id'],
                               blank_id=blank['id'],
                               answer=blank['studentAnswer'],
                               score=blank['score'],
                               status=blank['status'])
        db.session.add(exam_blank)

    for answer in question['answer']:
        if answer['answer'] == answer['studentAnswer']:
            score += int(answer['score'])
            answer['status'] = 'success'
        else:
            answer['status'] = 'error'
        exam_blank = ExamAnswer(student_name=examData['student_name'],
                                exam_id=examData['exam_id'],
                                answer_id=answer['id'],
                                answer=answer['studentAnswer'],
                                score=answer['score'],
                                status=answer['status'])
        db.session.add(exam_blank)
    exam_result = StudentResult(exam_id=examData['exam_id'],
                                student_name=examData['student_name'],
                                score=score,
                                submissionTime=datetime.date.today())
    db.session.add(exam_result)
    db.session.commit()
    return jsonify({'code': 200})


@student.route('/exam_detail', methods=['POST'])
def exam_detail():
    exam_id = request.json.get('exam_id')
    username = request.json.get('username')

    exam_data = StudentResult.query.filter_by(exam_id=exam_id, student_name=username).first()
    exam_single = ExamSingle.query.filter_by(exam_id=exam_id, student_name=username).all()
    singleList = []
    for single in exam_single:
        questionData = Single.query.filter_by(id=single.single_id).first()
        data = questionData.to_json()
        data['studentAnswer'] = single.answer
        data['status'] = single.status
        data['score'] = single.score
        singleList.append(data)

    exam_multiple = ExamMultiple.query.filter_by(exam_id=exam_id, student_name=username).all()
    multipleList = []
    for multiple in exam_multiple:
        questionData = Multiple.query.filter_by(id=multiple.multiple_id).first()
        data = questionData.to_json()
        data['studentAnswers'] = multiple.answer.split(',')
        data['studentAnswer'] = multiple.answer
        data['status'] = multiple.status
        data['score'] = multiple.score
        multipleList.append(data)

    exam_judgment = ExamJudgment.query.filter_by(exam_id=exam_id, student_name=username).all()
    judgmentList = []
    for judgment in exam_judgment:
        questionData = Judgment.query.filter_by(id=judgment.judgment_id).first()
        data = questionData.to_json()
        data['studentAnswer'] = judgment.answer
        data['status'] = judgment.status
        data['score'] = judgment.score
        judgmentList.append(data)

    exam_blank = ExamBlank.query.filter_by(exam_id=exam_id, student_name=username).all()
    blankList = []
    for blank in exam_blank:
        questionData = Blank.query.filter_by(id=blank.blank_id).first()
        data = questionData.to_json()
        data['studentAnswer'] = blank.answer
        data['status'] = blank.status
        data['score'] = blank.score
        blankList.append(data)

    exam_answer = ExamAnswer.query.filter_by(exam_id=exam_id, student_name=username).all()
    answerList = []
    for answer in exam_answer:
        questionData = Answer.query.filter_by(id=answer.answer_id).first()
        data = questionData.to_json()
        data['studentAnswer'] = answer.answer
        data['status'] = answer.status
        data['score'] = answer.score
        answerList.append(data)
    datas = {
        '单选题': singleList,
        '多选题': multipleList,
        '判断题': judgmentList,
        '填空题': blankList,
        '问答题': answerList,
        '考试信息': exam_data.to_json()
    }
    return jsonify(datas)
