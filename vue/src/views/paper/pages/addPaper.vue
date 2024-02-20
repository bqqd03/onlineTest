<template>
  <el-card >
    <template #header>
      <div class="card-header">
        <span>添加试卷</span>
        <el-button type="info" :icon="Back" @click="back">返回</el-button>
      </div>
    </template>


    <div style="margin: 5px 0 30px 80px;display: flex;justify-content: space-between;width: 85%">
      <div style=" display: flex;flex-direction: column;width: 40%">
        <div style=" display: flex;flex-direction: row;margin-bottom: 20px;align-items: center">
          <text style="margin-right: 10px;font-size: 15px;width: 80px">试卷代码</text>
          <el-input onkeypress='return( /[\d]/.test(String.fromCharCode(event.keyCode)))' v-model="options.paper_id" placeholder="请输入试卷代码" />
        </div>

        <div style=" display: flex;flex-direction: row;margin-bottom: 20px;align-items: center">
          <text style="margin-right: 10px;font-size: 15px;width: 80px">试卷名称</text>
          <el-input v-model="options.paper_name" placeholder="请输入试卷名称" />
        </div>

        <div style="display: flex;flex-direction: row;align-items: center;margin-bottom: 20px">
          <text style="margin-right: 10px;font-size: 15px;width: 80px">所属课程</text>
          <el-select v-model="options.course_id" style="width: 150px;margin-left: -14px" @change="getMenuList()" placeholder="请选择所属课程">
            <el-option
                v-for="item in course.options"
                :key="item.course_id"
                :label="item.course_name"
                :value="item.course_id" />
          </el-select>
        </div>

        <div style=" display: flex;flex-direction: row"  v-if="catalogs.showTree">
          <text style="margin-right: 23px;font-size: 15px;width: 80px">知识点</text>
          <div style="display: flex;flex-direction: column;margin-left: -33px">
            <div style="margin-bottom: 8px" v-for="catalog in catalogs.menuData" >
              <div style="display: flex;">
                <ArrowDownBold  v-if="catalog.show" style="height: 10px;width: 10px;margin-top: 7px;margin-right: 5px " />
                <ArrowRightBold v-else style="height: 10px;width: 10px;margin-top: 7px;margin-right: 5px "/>
                <span style="cursor: pointer;font-size: 15px" @click="catalogShow(catalog.id)">{{catalog.label}}</span>
              </div>
              <div style="margin-top: 5px">
                <el-checkbox-group v-if="catalog.show" v-for="item in catalog.children"  style="display: flex;margin-left: 20px;" v-model="options.knowledge_point">
                  <el-checkbox @change="getQuestionNum()" :label="item.id" style="font-size: 15px">{{ item.label }}</el-checkbox>
                </el-checkbox-group>
              </div>

            </div>
          </div>
        </div>
      </div>

      <div style="width: 50%;">
        <div style="display: flex;justify-content: space-between;margin-bottom: 40px;">
          <div>
            <text>题目数量：{{ options.num }}</text>
          </div>
          <div style="margin-right: 60px">
            <text>试卷总分：{{ options.score }}</text>
          </div>
        </div>
        <div style=" display: flex;justify-content: space-between;margin-bottom: 20px;">
          <text style="font-size: 18px">单选题（有{{ questionsNum.single }}道题）</text>
          <div style="margin-right: -50px">
            <text>每题</text>
            <el-input-number :controls="false" v-model.number="options.single_score" class="number_input"></el-input-number>
            <text>分，共</text>
            <el-input-number :max=questionsNum.single :controls="false" v-model.number="options.single_num" class="number_input"></el-input-number>
            <text>题</text>
          </div>
        </div>

        <div style=" display: flex;justify-content: space-between;margin-bottom: 20px;">
          <text style="font-size: 18px">多选题（有{{ questionsNum.multiple }}道题）</text>
          <div style="margin-right: -50px">
            <text>每题</text>
            <el-input-number :controls="false" v-model.number="options.multiple_score" class="number_input"></el-input-number>
            <text>分，共</text>
            <el-input-number :max=questionsNum.multiple :controls="false" v-model.number="options.multiple_num" class="number_input"></el-input-number>
            <text>题</text>
          </div>
        </div>

        <div style=" display: flex;justify-content: space-between;margin-bottom: 20px;">
          <text style="font-size: 18px">判断题（有{{ questionsNum.judgment }}道题）</text>
          <div style="margin-right: -50px">
            <text>每题</text>
            <el-input-number :controls="false" v-model.number="options.judgment_score" class="number_input"></el-input-number>
            <text>分，共</text>
            <el-input-number :max=questionsNum.judgment :controls="false" v-model.number="options.judgment_num" class="number_input"></el-input-number>
            <text>题</text>
          </div>
        </div>

        <div style=" display: flex;justify-content: space-between;margin-bottom: 20px;">
          <text style="font-size: 18px">填空题（有{{ questionsNum.blank }}道题）</text>
          <div style="margin-right: -50px">
            <text>每题</text>
            <el-input-number :controls="false" v-model.number="options.blank_score" class="number_input"></el-input-number>
            <text>分，共</text>
            <el-input-number :max=questionsNum.blank :controls="false" v-model.number="options.blank_num" class="number_input"></el-input-number>
            <text>题</text>
          </div>
        </div>

        <div style=" display: flex;justify-content: space-between;margin-bottom: 20px;">
          <text style="font-size: 18px">问答题（有{{ questionsNum.answer }}道题）</text>
          <div style="margin-right: -50px">
            <text>每题</text>
            <el-input-number :controls="false"  v-model.number="options.answer_score" class="number_input"></el-input-number>
            <text>分，共</text>
            <el-input-number :max=questionsNum.answer :controls="false"  v-model.number="options.answer_num" class="number_input"></el-input-number>
            <text>题</text>
          </div>
        </div>

      </div>
    </div>
    <el-button @click="savePaper()" type="primary" :icon="FolderAdd" style="position: absolute;left: 45%;">保存</el-button>
  </el-card>
</template>

<script setup>
import {onMounted, reactive, watchEffect} from 'vue'
import { useRouter } from 'vue-router'
import { Back } from '@element-plus/icons-vue'
import { FolderAdd } from '@element-plus/icons-vue'
import https from "@/apis/axio"
import { ElMessage } from "element-plus"

let catalogs=reactive({
  showTree: false,
  menuData:[]
})

const router = useRouter()
const options=reactive({
  paper_name:'',
  paper_id:'',
  course_id:'',
  knowledge_point:[],
  score:[],
  num:[],
  single_num:0,
  single_score:0,
  multiple_num:0,
  multiple_score:0,
  judgment_num:0,
  judgment_score:0,
  blank_num:0,
  blank_score:0,
  answer_num:0,
  answer_score:0
})
const questionsNum=reactive({
  single:0,
  multiple:0,
  judgment:0,
  blank:0,
  answer:0
})
const course=reactive({
  options:[]
})

watchEffect(() => {
  options.score = options.single_score*options.single_num  + options.multiple_score*options.multiple_num + options.judgment_score*options.judgment_num + options.blank_score*options.blank_num + options.answer_score*options.answer_num
  options.num = options.single_num + options.multiple_num + options.judgment_num + options.blank_num + options.answer_num
})

onMounted(()=> {
  https.post('/teacher/get_courses',{'username':JSON.parse(localStorage.getItem('token')).username}).then(res => {
    course.options = res.data
  })
})

function back() {
  router.push("/paper")
}

function getMenuList () {
  catalogs.showTree = true
  https.post("/teacher/get_catalog",{'course':options.course_id} ).then(res => {
    res.data.forEach(item=>{
      item.show=false
    })
    catalogs.menuData = res.data
  })

}
function catalogShow(id) {
  catalogs.menuData.forEach(item=>{
    if (item.id === id){
      item.show = item.show === false;
    } else {
      item.show = false
    }
  })
}

function getQuestionNum() {
  console.log(options.knowledge_point)
  https.post("/teacher/question_num",{'knowledge_id':options.knowledge_point} ).then(res => {
    questionsNum.single=res.data['单选题']
    questionsNum.multiple=res.data['多选题']
    questionsNum.judgment=res.data['判断题']
    questionsNum.blank=res.data['填空题']
    questionsNum.answer=res.data['问答题']
  })
}

function savePaper(){
  https.post('/teacher/add_paper', options).then(res=>{
    if (res.data.code === 200){
      ElMessage.success('添加成功')
      back()
    } else {
      ElMessage.error(res.data.message)
    }
  })
}
</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 20px;
}
.el-card{
  height: 100%;
}
.fistBox :hover{
  background-color: #F5F5F5;
}
.number_input{
  width: 45px;
  height: 28px;
  margin: 0 8px
}
</style>
