import random
import datetime

from flask import request, jsonify

from . import teacher
from .. import db
from ..models import User, Course, Catalog, Single, Multiple, Judgment, Blank, Answer, Paper, StudentClass, ClassInfo, \
    Exam


# 获取课程
@teacher.route('/get_courses', methods=['POST'])
def get_courses():
    username = request.json.get('username')
    user_catalog = Course.query.filter_by(teacher_name=username).all()
    data = []
    for i in user_catalog:
        data.append(i.to_json())
    return jsonify(data)


@teacher.route('/get_catalog', methods=['POST'])
def get_catalog():
    course = request.json.get('course')
    catalog_data = Catalog.query.filter_by(course_id=course, pid=None).all()
    datas = []
    for i in catalog_data:
        data = i.to_json()
        pid = data['id']
        children = []
        context_data = Catalog.query.filter_by(pid=pid).all()
        for j in context_data:
            singles = Single.query.filter_by(knowledge_point=j.id).count()
            multiple = Multiple.query.filter_by(knowledge_point=j.id).count()
            judgment = Judgment.query.filter_by(knowledge_point=j.id).count()
            blank = Blank.query.filter_by(knowledge_point=j.id).count()
            answer = Answer.query.filter_by(knowledge_point=j.id).count()
            if singles + multiple + judgment + blank + answer != 0:
                j.isEdit = '1'
            children.append(j.to_json())
        data['children'] = children
        datas.append(data)
    return jsonify(datas)


@teacher.route('/add_catalog', methods=['POST'])
def add_catalog():
    catalog_id = request.json.get('id')
    label = request.json.get('label')
    pid = request.json.get('pid')
    course_id = request.json.get('course_id')
    isEdit = request.json.get('isEdit')

    if catalog_id == '':
        return jsonify({'code': 400, 'message': '请填写代码'})
    elif label == '':
        return jsonify({'code': 400, 'message': '请填写名称'})
    id_data = Catalog.query.filter_by(id=catalog_id).first()

    if id_data is not None:
        return jsonify({'code': 400, 'message': '代码重复'})
    label_data = Catalog.query.filter_by(label=label).first()
    if label_data is not None:
        return jsonify({'code': 400, 'message': '名称重复'})
    catalog_data = Catalog(id=catalog_id,
                           label=label,
                           pid=pid,
                           course_id=course_id,
                           isEdit=isEdit)

    db.session.add(catalog_data)
    db.session.commit()
    return jsonify({'code': 200})


@teacher.route('/edit_catalog', methods=['POST'])
def edit_catalog():
    catalog_id = request.json.get('id')
    label = request.json.get('label')

    if label == '':
        return jsonify({'code': 400, 'message': '请填写知识点名称'})
    catalog_data = Catalog.query.filter_by(id=catalog_id).first()
    catalog_name = Catalog.query.filter_by(label=label).first()
    if catalog_name is not None and catalog_name.id != catalog_id:
        return jsonify({'code': 400, 'message': '知识点名称重复'})
    catalog_data.label = label
    db.session.commit()
    return jsonify({'code': 200})


@teacher.route('/delete_catalog', methods=['POST'])
def delete_catalog():
    catalog_id = request.json.get('catalog_id')
    catalog_data = Catalog.query.filter_by(id=catalog_id).first()
    db.session.delete(catalog_data)
    db.session.commit()
    return jsonify({'code': 200})


@teacher.route('/get_singles', methods=['POST'])
def get_singles():
    identify_id = request.json.get('identify_id')
    identify_type = request.json.get('identify_type')
    datas = []

    if identify_type == '课程':
        single_data = Single.query.filter_by(course_id=identify_id).all()
    else:
        single_data = Single.query.filter_by(knowledge_point=identify_id).all()

    for i in single_data:
        data = i.to_json()
        context = Catalog.query.filter_by(id=data['knowledge_point']).first()
        data['knowledge_label'] = context.label
        datas.append(data)
    return jsonify(datas)


@teacher.route('/get_multiples', methods=['POST'])
def get_multiples():
    identify_id = request.json.get('identify_id')
    identify_type = request.json.get('identify_type')
    datas = []

    if identify_type == '课程':
        multiple_data = Multiple.query.filter_by(course_id=identify_id).all()
    else:
        multiple_data = Multiple.query.filter_by(knowledge_point=identify_id).all()

    for i in multiple_data:
        data = i.to_json()
        context = Catalog.query.filter_by(id=data['knowledge_point']).first()
        data['knowledge_label'] = context.label
        data['answers'] = data['answer'].split(',')
        datas.append(data)
    return jsonify(datas)


@teacher.route('/get_judgements', methods=['POST'])
def get_judgements():
    identify_id = request.json.get('identify_id')
    identify_type = request.json.get('identify_type')
    datas = []

    if identify_type == '课程':
        judgement_data = Judgment.query.filter_by(course_id=identify_id).all()
    else:
        judgement_data = Judgment.query.filter_by(knowledge_point=identify_id).all()

    for i in judgement_data:
        data = i.to_json()
        context = Catalog.query.filter_by(id=data['knowledge_point']).first()
        data['knowledge_label'] = context.label
        datas.append(data)
    return jsonify(datas)


@teacher.route('/get_blanks', methods=['POST'])
def get_blanks():
    identify_id = request.json.get('identify_id')
    identify_type = request.json.get('identify_type')
    datas = []

    if identify_type == '课程':
        blank_data = Blank.query.filter_by(course_id=identify_id).all()
    else:
        blank_data = Blank.query.filter_by(knowledge_point=identify_id).all()

    for i in blank_data:
        data = i.to_json()
        context = Catalog.query.filter_by(id=data['knowledge_point']).first()
        data['knowledge_label'] = context.label
        datas.append(data)
    return jsonify(datas)


@teacher.route('/get_answers', methods=['POST'])
def get_answers():
    identify_id = request.json.get('identify_id')
    identify_type = request.json.get('identify_type')
    datas = []

    if identify_type == '课程':
        answer_data = Answer.query.filter_by(course_id=identify_id).all()
    else:
        answer_data = Answer.query.filter_by(knowledge_point=identify_id).all()

    for i in answer_data:
        data = i.to_json()
        context = Catalog.query.filter_by(id=data['knowledge_point']).first()
        data['knowledge_label'] = context.label
        datas.append(data)
    return jsonify(datas)


@teacher.route('/search_questions', methods=['POST'])
def search_questions():
    identify_id = request.json.get('identify_id')
    identify_type = request.json.get('identify_type')
    searchDegree = request.json.get('searchDegree')
    searchStyle = request.json.get('searchStyle')
    datas = {}

    # 定义一个字典，存储不同类型的查询类
    query_classes = {
        '单选': Single,
        '多选': Multiple,
        '判断': Judgment,
        '填空': Blank,
        '问答': Answer
    }

    # 定义一个函数，根据查询类和过滤条件，返回数据列表
    def get_data_list(queryClass, degree=None):
        # 根据 identify_type 和 identify_id 过滤数据
        if identify_type == '课程':
            query = queryClass.query.filter_by(course_id=identify_id)
        else:
            query = queryClass.query.filter_by(knowledge_point=identify_id)
        # 如果有 degree 条件，再次过滤数据
        if degree is not None:
            query = query.filter_by(degree=degree)
        # 获取所有数据
        dataList = query.all()
        # 转换为 JSON 格式
        json_list = []
        for data in dataList:
            json_data = data.to_json()
            # 如果是多选题，还要分割答案
            if queryClass == Multiple:
                json_data['answers'] = json_data['answer'].split(',')
            json_list.append(json_data)
        return json_list

    # 定义一个函数，根据查询类，将数据列表添加到 datas 字典中
    def add_data_to_datas(queryClass, dataList):
        # 根据查询类的名称，获取 datas 的键
        key = queryClass.__name__.lower() + 's'
        # 将数据列表添加到 datas 字典中
        datas[key] = dataList

    # 如果 searchDegree 和 searchStyle 都是 '全部'，则查询所有类型的数据
    if searchDegree == '全部' and searchStyle == '全部':
        for query_class in query_classes.values():
            data_list = get_data_list(query_class)
            add_data_to_datas(query_class, data_list)
    # 如果 searchDegree 是 '全部'，则查询指定类型的数据
    elif searchDegree == '全部':
        query_class = query_classes[searchStyle]
        data_list = get_data_list(query_class)
        add_data_to_datas(query_class, data_list)
    # 如果 searchStyle 是 '全部'，则查询指定难度的所有类型的数据
    elif searchStyle == '全部':
        for query_class in query_classes.values():
            data_list = get_data_list(query_class, degree=searchDegree)
            add_data_to_datas(query_class, data_list)
    # 否则，查询指定难度和类型的数据
    else:
        query_class = query_classes[searchStyle]
        data_list = get_data_list(query_class, degree=searchDegree)
        add_data_to_datas(query_class, data_list)

    for i in datas:
        for j in datas[i]:
            context = Catalog.query.filter_by(id=j['knowledge_point']).first()
            j['knowledge_label'] = context.label
    return jsonify(datas)


@teacher.route('/add_question', methods=['POST'])
def add_question():
    # 定义一个字典，存储不同类型的数据类
    data_classes = {
        '单选题': Single,
        '多选题': Multiple,
        '判断题': Judgment,
        '填空题': Blank,
        '问答题': Answer
    }

    # 定义一个函数，根据请求参数，创建数据对象
    def create_data_object(data_class):
        # 获取请求参数
        question = request.json.get('question')
        optionsA = request.json.get('optionsA')
        optionsB = request.json.get('optionsB')
        optionsC = request.json.get('optionsC')
        optionsD = request.json.get('optionsD')
        answer = request.json.get('answer')
        answers = request.json.get('answers')
        analysis = request.json.get('analysis')
        degree = request.json.get('degree')
        course_id = request.json.get('course_id')
        knowledge_point = request.json.get('knowledge_point')
        if data_class == Single or data_class == Multiple:
            # 创建数据对象
            data_object = data_class(question=question,
                                     optionsA=optionsA,
                                     optionsB=optionsB,
                                     optionsC=optionsC,
                                     optionsD=optionsD,
                                     answer=answer,
                                     analysis=analysis,
                                     degree=degree,
                                     course_id=course_id,
                                     knowledge_point=knowledge_point)
        else:
            data_object = data_class(question=question,
                                     answer=answer,
                                     analysis=analysis,
                                     degree=degree,
                                     course_id=course_id,
                                     knowledge_point=knowledge_point)
        # 如果是多选题，还要将答案列表转换为字符串
        if data_class == Multiple:
            data_object.answer = ','.join(answers)
        return data_object

    # 定义一个函数，根据数据对象，添加到数据库会话中
    def add_data_to_session(data_object):
        db.session.add(data_object)

    # 获取请求参数中的题目类型
    question_type = request.json.get('type')
    # 根据数据对象，添加到数据库会话中
    add_data_to_session(create_data_object(data_classes[question_type]))
    # 提交数据库会话
    db.session.commit()

    return jsonify({'code': 200})


@teacher.route('/edit_question', methods=['POST'])
def edit_question():
    # 定义一个字典，存储不同类型的数据类
    data_classes = {
        '单选题': Single,
        '多选题': Multiple,
        '判断题': Judgment,
        '填空题': Blank,
        '问答题': Answer
    }

    # 定义一个函数，根据请求参数，创建数据对象
    def edit_data_object(data_class):
        # 获取请求参数
        question_id = request.json.get('id')
        question = request.json.get('question')
        answer = request.json.get('answer')
        analysis = request.json.get('analysis')
        degree = request.json.get('degree')
        course_id = request.json.get('course_id')
        knowledge_point = request.json.get('knowledge_point')
        # 创建数据对象
        data_object = data_class.query.filter_by(id=question_id).first()
        # 如果是多选题，还要将答案列表转换为字符串
        data_object.question = question
        if data_class == Multiple:
            answers = request.json.get('answers')
            data_object.answer = ','.join(answers)
        else:
            data_object.answer = answer
        if data_class == Single or data_class == Multiple:
            optionsA = request.json.get('optionsA')
            optionsB = request.json.get('optionsB')
            optionsC = request.json.get('optionsC')
            optionsD = request.json.get('optionsD')
            data_object.optionsA = optionsA
            data_object.optionsB = optionsB
            data_object.optionsA = optionsC
            data_object.optionsA = optionsD
        data_object.analysis = analysis
        data_object.degree = degree
        data_object.course_id = course_id
        data_object.knowledge_point = knowledge_point
        return data_object

    # 获取请求参数中的题目类型
    question_type = request.json.get('type')
    # 根据数据类，创建数据对象
    edit_data_object(data_classes[question_type])
    # 提交数据库会话
    db.session.commit()

    return jsonify({'code': 200})


@teacher.route('/delete_question', methods=['POST'])
def delete_question():
    question_id = request.json.get('question_id')
    question_type = request.json.get('question_type')
    data_classes = {
        '单选题': Single,
        '多选题': Multiple,
        '判断题': Judgment,
        '填空题': Blank,
        '问答题': Answer
    }
    question_data = data_classes[question_type].query.filter_by(id=question_id).first()
    db.session.delete(question_data)
    db.session.commit()
    return jsonify({'code': 200})


@teacher.route('/question_num', methods=['POST'])
def question_num():
    knowledge_id = request.json.get('knowledge_id')
    data_classes = {
        '单选题': Single,
        '多选题': Multiple,
        '判断题': Judgment,
        '填空题': Blank,
        '问答题': Answer
    }
    datas = {}
    for i in data_classes:
        data_num = 0
        for j in knowledge_id:
            data_num += data_classes[i].query.filter_by(knowledge_point=j).count()
        datas[i] = data_num
    return jsonify(datas)


@teacher.route('/get_paper', methods=['POST'])
def get_paper():
    teacher_name = request.json.get('teacher')
    course = Course.query.filter_by(teacher_name=teacher_name).all()
    datas = []
    for item in course:
        data = Paper.query.filter_by(course_id=item.course_id).all()
        for i in data:
            paper_data = i.to_json()
            paper_data['course_name'] = item.course_name
            catalog_name = []
            for j in paper_data['knowledge_point'].split(','):
                catalog = Catalog.query.filter_by(id=j).first()
                catalog_name.append(catalog.label)
            paper_data['catalog_name'] = catalog_name
            datas.append(paper_data)

    return jsonify(datas)


@teacher.route('/add_paper', methods=['POST'])
def add_paper():
    paper_name = request.json.get('paper_name')
    paper_id = request.json.get('paper_id')
    course_id = request.json.get('course_id')
    knowledge_point = request.json.get('knowledge_point')
    paper_score = request.json.get('score')
    paper_num = request.json.get('num')

    question_type = {
        'single': Single,
        'multiple': Multiple,
        'judgment': Judgment,
        'blank': Blank,
        'answer': Answer
    }
    paper_question = {}
    question_score = {}

    if paper_id == '':
        return jsonify({'code': 400, 'message': '请填写试卷代码'})
    elif paper_name == '':
        return jsonify({'code': 400, 'message': '请填写试卷名称'})
    id_data = Paper.query.filter_by(paper_id=paper_id).first()
    if id_data is not None:
        return jsonify({'code': 400, 'message': '试卷代码重复'})
    label_data = Paper.query.filter_by(paper_name=paper_name).first()
    if label_data is not None:
        return jsonify({'code': 400, 'message': '试卷名称重复'})

    for i in question_type:
        question_id = []
        for j in knowledge_point:
            question_data = question_type[i].query.filter_by(knowledge_point=j).all()
            question_id += question_data
        class_id = [str(i.id) for i in question_id]
        class_num = request.json.get(i + '_num')
        class_score = request.json.get(i + '_score')
        if class_num != 0:
            paper_question[i] = ','.join(random.sample(class_id, class_num))
            question_score[i] = class_score
        else:
            paper_question[i] = ''
            question_score[i] = ''

    paper_data = Paper(paper_id=paper_id,
                       paper_name=paper_name,
                       course_id=course_id,
                       knowledge_point=','.join(knowledge_point),
                       paper_score=paper_score,
                       paper_num=paper_num,
                       single=paper_question['single'],
                       single_score=question_score['single'],
                       multiple=paper_question['multiple'],
                       multiple_score=question_score['multiple'],
                       judgment=paper_question['judgment'],
                       judgment_score=question_score['judgment'],
                       blank=paper_question['blank'],
                       blank_score=question_score['blank'],
                       answer=paper_question['answer'],
                       answer_score=question_score['answer'])
    db.session.add(paper_data)
    db.session.commit()
    return jsonify({'code': 200})


@teacher.route('/paper_detail', methods=['POST'])
def paper_detail():
    paper_id = request.json.get('paper_id')
    datas = {}
    paper_data = Paper.query.filter_by(id=paper_id).first()
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
                context = Catalog.query.filter_by(id=question['knowledge_point']).first()
                question['knowledge_label'] = context.label
                if item == '多选题':
                    question['answers'] = question['answer'].split(',')
                data.append(question)
        datas[item] = data
    return jsonify(datas)


@teacher.route('/edit_paper', methods=['POST'])
def edit_paper():
    data_id = request.json.get('id')
    paper_id = request.json.get('paper_id')
    paper_name = request.json.get('paper_name')

    if paper_id == '':
        return jsonify({'code': 400, 'message': '请填写试卷代码'})
    elif paper_name == '':
        return jsonify({'code': 400, 'message': '请填写试卷名称'})
    paper_data = Paper.query.filter_by(id=data_id).first()
    id_data = Paper.query.filter_by(paper_id=paper_id).first()
    if id_data is not None and id_data.id != data_id:
        return jsonify({'code': 400, 'message': '试卷代码重复'})
    name_data = Paper.query.filter_by(paper_name=paper_name).first()
    if name_data is not None and name_data.id != data_id:
        return jsonify({'code': 400, 'message': '试卷名称重复'})
    paper_data.paper_id = paper_id
    paper_data.paper_name = paper_name
    db.session.commit()
    return jsonify({'code': 200})


@teacher.route('/delete_paper', methods=['POST'])
def delete_paper():
    data_id = request.json.get('data_id')
    paper_data = Paper.query.filter_by(id=data_id).first()
    db.session.delete(paper_data)
    db.session.commit()
    return jsonify({'code': 200})


@teacher.route('/search_paper', methods=['POST'])
def search_paper():
    paper_name = request.json.get('paper_name')
    paper_id = request.json.get('paper_id')
    course_id = request.json.get('course_id')
    data = []

    # 创建一个字典，存储非空的查询条件
    query_dict = {}
    if paper_name != '':
        query_dict['paper_name'] = paper_name
    if paper_id != '':
        query_dict['paper_id'] = paper_id
    if course_id != '':
        query_dict['course_id'] = course_id

    # 使用 kwargs 参数，传递字典给 filter_by 方法
    paper_data = Paper.query.filter_by(**query_dict).all()
    for i in paper_data:
        paper = i.to_json()
        course = Course.query.filter_by(course_id=i.course_id).first()
        paper['course_name'] = course.course_name
        catalog_name = []
        for j in paper['knowledge_point'].split(','):
            catalog = Catalog.query.filter_by(id=j).first()
            catalog_name.append(catalog.label)
        paper['catalog_name'] = catalog_name
        data.append(paper)
    return jsonify(data)


@teacher.route('/class_list', methods=['POST'])
def class_list():
    username = request.json.get('username')
    course_data = Course.query.filter_by(teacher_name=username).all()
    data = []
    for i in course_data:
        class_data = ClassInfo.query.filter_by(course_id=i.course_id).all()
        for j in class_data:
            data.append(j.to_json())

    for h in data:
        stu_num = StudentClass.query.filter_by(class_id=h['class_code'], confirm='1').count()
        h['stu_num'] = stu_num
        course_name = Course.query.filter_by(course_id=h['course_id']).first()
        h['course_name'] = course_name.course_name
    return jsonify(data)


@teacher.route('/add_class', methods=['POST'])
def add_class():
    class_name = request.json.get('class_name')
    class_code = request.json.get('class_code')
    course_id = request.json.get('course_id')

    if course_id == '':
        return jsonify({'code': 400, 'message': '请选择所属课程'})
    if class_name == '':
        return jsonify({'code': 400, 'message': '请输入班级名称'})
    else:
        class_data = ClassInfo.query.filter_by(class_name=class_name).first()
        if class_data is not None:
            return jsonify({'code': 400, 'message': '班级名称已存在'})
    if class_code == '':
        return jsonify({'code': 400, 'message': '请输入班级码'})
    else:
        class_data = ClassInfo.query.filter_by(class_code=class_code).first()
        if class_data is not None:
            return jsonify({'code': 400, 'message': '班级码已存在'})

    exercise_data = ClassInfo(class_name=class_name,
                              class_code=class_code,
                              course_id=course_id)
    db.session.add(exercise_data)
    db.session.commit()
    return jsonify({'code': 200})


@teacher.route('/class_student', methods=['POST'])
def class_student():
    class_id = request.json.get('class_id')
    class_data = ClassInfo.query.filter_by(class_id=class_id).first()
    student_data = StudentClass.query.filter_by(class_id=class_data.class_code, confirm='1').all()
    data = []
    for i in student_data:
        stu_data = User.query.filter_by(user_id=i.to_json()['student_id']).first()
        data.append(stu_data.to_json())
    return jsonify({'data': data, 'class_name': class_data.class_name})


@teacher.route('/applicant', methods=['POST'])
def applicant():
    class_id = request.json.get('class_id')
    class_data = ClassInfo.query.filter_by(class_id=class_id).first()
    datas = []
    applicant_data = StudentClass.query.filter_by(class_id=class_data.to_json()['class_code'], confirm='0').all()
    for i in applicant_data:
        applicant_info = i.to_json()
        student_data = User.query.filter_by(user_id=applicant_info['student_id']).first()
        student_info = student_data.to_json()
        data = {'user_id': student_info['user_id'], 'username': student_info['username'],
                'avatar': student_info['avatar'], 'confirm': applicant_info['confirm']}
        datas.append(data)
    return jsonify(datas)


@teacher.route('/applicant_confirm', methods=['POST'])
def applicant_confirm():
    user_id = request.json.get('user_id')
    class_id = request.json.get('class_id')
    type = request.json.get('type')
    class_data = ClassInfo.query.filter_by(class_id=class_id).first()
    student_data = StudentClass.query.filter_by(student_id=user_id, class_id=class_data.to_json()['class_code']).first()
    student_data.confirm = type
    db.session.commit()

    return jsonify({'code': 200})


@teacher.route('/get_class', methods=['POST'])
def get_class():
    course_id = request.json.get('course_id')
    data = []
    all_class = []
    class_data = ClassInfo.query.filter_by(course_id=course_id).all()
    for i in class_data:
        all_class.append(i.class_code)
        data.append(i.to_json())

    return jsonify(data)


@teacher.route('/add_exam', methods=['POST'])
def add_exam():
    exam_id = request.json.get('exam_id')
    exam_name = request.json.get('exam_name')
    exam_course = request.json.get('exam_course')
    exam_class = request.json.get('exam_class')
    exam_type = request.json.get('exam_type')
    exam_date = request.json.get('exam_date')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    answer_time = request.json.get('answer_time')
    attention = request.json.get('attention')

    if exam_id == '':
        return jsonify({'code': 400, 'message': '请填写考试编码'})
    else:
        exam = Exam.query.filter_by(exam_id=exam_id).first()
        if exam is not None:
            return jsonify({'code': 400, 'message': '考试编码重复'})

    if exam_name == '':
        return jsonify({'code': 400, 'message': '请填写考试名称'})
    else:
        exam = Exam.query.filter_by(exam_name=exam_name).first()
        if exam is not None:
            return jsonify({'code': 400, 'message': '考试名称重复'})

    if exam_course == '':
        return jsonify({'code': 400, 'message': '请选择考试课程'})

    if exam_class == '':
        return jsonify({'code': 400, 'message': '请选择考试班级'})

    if exam_type == '':
        return jsonify({'code': 400, 'message': '请选择考试类型'})

    if exam_date == '':
        return jsonify({'code': 400, 'message': '请选择考试日期'})

    if start_time == '':
        return jsonify({'code': 400, 'message': '请选择开始时间'})

    if end_time == '':
        return jsonify({'code': 400, 'message': '请选择结束时间'})

    if answer_time == '':
        return jsonify({'code': 400, 'message': '请选择答题时间'})
    paperNum = Paper.query.filter_by(course_id=exam_course).count()
    if paperNum == 0:
        return jsonify({'code': 400, 'message': '该课程没有试卷'})

    exam_data = Exam(exam_id=exam_id,
                     exam_name=exam_name,
                     exam_course=exam_course,
                     exam_class=exam_class,
                     exam_type=exam_type,
                     exam_date=exam_date,
                     start_time=start_time,
                     end_time=end_time,
                     answer_time=answer_time,
                     attention=attention)
    db.session.add(exam_data)
    db.session.commit()

    return jsonify({'code': 200})


@teacher.route('/exam_info', methods=['POST'])
def exam_info():
    exam_id = request.json.get('exam_id')
    exam_data = Exam.query.filter_by(exam_id=exam_id).first()
    course = Course.query.filter_by(course_id=exam_data.exam_course).first()
    paper_data = Paper.query.filter_by(course_id=exam_data.exam_course).all()
    paperList = []
    for paper in paper_data:
        paperList.append(paper.to_json())

    data = {'exam_id': exam_data.exam_id, 'exam_name': exam_data.exam_name, 'exam_course': course.course_name,
            'exam_type': exam_data.exam_type, 'paper': paperList}

    return jsonify(data)


@teacher.route('/exam_paper', methods=['POST'])
def exam_paper():
    exam_id = request.json.get('exam_id')
    exam_paper = request.json.get('exam_paper')
    exam_score = request.json.get('exam_score')
    exam_data = Exam.query.filter_by(exam_id=exam_id).first()
    exam_data.exam_paper = exam_paper
    exam_data.exam_score = exam_score
    db.session.commit()

    return jsonify({'code': 200})


@teacher.route('/get_exam', methods=['POST'])
def get_exam():
    teacher_name = request.json.get('teacher')
    course = Course.query.filter_by(teacher_name=teacher_name).all()
    datas = []

    current_datetime = datetime.datetime.now()
    dayDate = datetime.date.today()
    current_time = current_datetime.time()

    for item in course:
        data = Exam.query.filter_by(exam_course=item.course_id).all()
        for i in data:
            exam_data = i.to_json()
            exam_data['course_name'] = item.course_name

            if dayDate > i.exam_date:
                exam_data['situation'] = '已结束'
            elif dayDate == i.exam_date:
                if current_time < i.start_time:
                    exam_data['situation'] = '未开始'
                elif i.start_time <= current_time <= i.end_time:
                    exam_data['situation'] = '进行中'
                elif current_time > i.end_time:
                    exam_data['situation'] = '已结束'
            elif dayDate < i.exam_date:
                exam_data['situation'] = '未开始'

            datas.append(exam_data)
    return jsonify(datas)


@teacher.route('/edit_exam', methods=['POST'])
def edit_exam():
    data_id = request.json.get('id')
    exam_id = request.json.get('exam_id')
    exam_name = request.json.get('exam_name')
    exam_date = request.json.get('exam_date')
    exam_class = request.json.get('exam_class')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    answer_time = request.json.get('answer_time')

    if exam_id == '':
        return jsonify({'code': 400, 'message': '请填写考试代码'})
    elif exam_name == '':
        return jsonify({'code': 400, 'message': '请填写考试名称'})
    elif exam_date == '':
        return jsonify({'code': 400, 'message': '请填写考试日期'})
    elif exam_class == '':
        return jsonify({'code': 400, 'message': '请选择考试班级'})
    elif answer_time == '':
        return jsonify({'code': 400, 'message': '请输入答题时间'})
    elif start_time == '':
        return jsonify({'code': 400, 'message': '请选择开始时间'})
    elif end_time == '':
        return jsonify({'code': 400, 'message': '请选择结束时间'})

    id_data = Exam.query.filter_by(exam_id=exam_id).first()
    if id_data is not None and id_data.id != data_id:
        return jsonify({'code': 400, 'message': '考试代码重复'})
    name_data = Exam.query.filter_by(exam_name=exam_name).first()
    if name_data is not None and name_data.id != data_id:
        return jsonify({'code': 400, 'message': '考试名称重复'})
    exam_data = Exam.query.filter_by(id=data_id).first()
    exam_data.exam_id = exam_id
    exam_data.exam_name = exam_name
    exam_data.exam_date = exam_date
    exam_data.exam_class = exam_class
    exam_data.start_time = start_time
    exam_data.end_time = end_time
    exam_data.answer_time = answer_time
    db.session.commit()
    return jsonify({'code': 200})


@teacher.route('/delete_exam', methods=['POST'])
def delete_exam():
    data_id = request.json.get('data_id')
    exam_data = Exam.query.filter_by(id=data_id).first()
    db.session.delete(exam_data)
    db.session.commit()
    return jsonify({'code': 200})
