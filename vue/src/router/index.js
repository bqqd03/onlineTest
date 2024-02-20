// 路由文件
import { createRouter, createWebHistory } from "vue-router";


const routes = [
    {
        path: "/login",
        name: "login",
        component: () => import("../views/Login.vue")
    }, {
        path: "/register",
        name: "register",
        component: () => import("../views/Register.vue")
    },{
        path: "/",
        name: "main",
        redirect:'/login',
        component: () => import("../views/main/Main.vue"),
        children:[{
            path: "/home",
            name: "home",
            component: () => import("../views/home.vue")
        },{
            path: "/questions",
            name: "questions",
            component: () => import("../views/questions/index.vue")
        },{
            path: "/add_question",
            name: "add_question",
            component: () => import("../views/questions/pages/addQuestion.vue")
        },{
            path: "/edit_question",
            name: "edit_question",
            component: () => import("../views/questions/pages/editQuestion.vue")
        },{
            path: "/paper",
            name: "paper",
            component: () => import("../views/paper/index.vue")
        },{
            path: "/add_paper",
            name: "add_paper",
            component: () => import("../views/paper/pages/addPaper.vue")
        },{
            path: "/teacher_exam",
            name: "teacher_exam",
            component: () => import("../views/teacherExam/index.vue")
        },{
            path: "/add_exam",
            name: "add_exam",
            component: () => import("../views/teacherExam/pages/addExam.vue")
        },{
            path: "/class_control",
            name: "class_control",
            component: () => import("../views/classControl/index.vue")
        },{
            path: "/class_student",
            name: "class_student",
            component: () => import("../views/classControl/pages/classStudent.vue")
        },{
            path: "/student_class",
            name: "student_class",
            component: () => import("../views/studentClass/index.vue")
        },{
            path: "/select_paper",
            name: "select_paper",
            component: () => import("../views/teacherExam/pages/selectPaper.vue")
        },{
            path: "/personal",
            name: "personal",
            component: () => import("../views/personal_center/index.vue")
        },{
            path: "/student_exam",
            name: "student_exam",
            component: () => import("../views/studentExam/index.vue")
        }]
    }, {
        path: "/detail_paper",
        name: "detail_paper",
        component: () => import("../views/paper/pages/detailPaper.vue")
    }, {
        path: "/exam_paper",
        name: "exam_paper",
        component: () => import("../views/studentExam/pages/examPaper.vue")
    }, {
        path: "/detail_exam",
        name: "detail_exam",
        component: () => import("../views/studentExam/pages/detailExam.vue")
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;
