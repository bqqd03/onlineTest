<template>
  <el-card >
    <template #header>
      <div class="card-header">
        <span>修改{{options.type}}</span>
        <el-button type="info" :icon="Back" @click="back">返回</el-button>
      </div>
    </template>

    <div style="margin-top: 5px;display: flex;justify-content: space-between;margin-bottom: 20px;width: 1000px">
      <div style=" display: flex;flex-direction: column;width: 500px">
        <div style=" display: flex;flex-direction: row;margin-bottom: 20px;align-items: center">
          <text style="margin-right: 10px;font-size: 15px;width: 80px">题目名称</text>
          <el-input v-model="options.question" placeholder="请输入题目名称" rows="3" type="textarea" />
        </div>
        <div style=" display: flex;flex-direction: row;margin-bottom: 20px;align-items: center">
          <text style="margin-right: 10px;font-size: 15px;width: 80px">题目答案</text>
          <el-radio-group style="margin-left: -13px" v-model="options.answer" v-if="options.type === '单选题'">
            <el-radio-button label="A" />
            <el-radio-button label="B" />
            <el-radio-button label="C" />
            <el-radio-button label="D" />
          </el-radio-group>
          <el-checkbox-group style="margin-left: -13px" v-model="options.answers" v-else-if="options.type === '多选题'">
            <el-checkbox-button v-for="item in selects" :key="item" :label="item"/>
          </el-checkbox-group>
          <el-radio-group style="margin-left: -13px" v-model="options.answer" v-else-if="options.type === '判断题'">
            <el-radio label="T" size="large">T</el-radio>
            <el-radio label="F" size="large">F</el-radio>
          </el-radio-group>
          <el-input v-model="options.answer" v-else placeholder="请输入答案" />
        </div>
        <div style=" display: flex;justify-content: space-between;margin-bottom: 20px">
          <div style=" display: flex;flex-direction: row;align-items: center">
            <text style="margin-right: 10px;font-size: 15px;width: 80px">难度选择</text>
            <el-select v-model="options.degree" style="width: 130px;margin-left: -13px">
              <el-option
                  v-for="item in degrees"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value" />
            </el-select>
          </div>
        </div>
        <div style=" display: flex;flex-direction: row;margin-bottom: 20px">
          <text style="margin-right: 10px;font-size: 15px;width: 80px">题目分析</text>
          <el-input v-model="options.analysis" placeholder="请输入题目分析" rows="3" type="textarea" />
        </div>
        <div style=" display: flex;flex-direction: row;align-items: center;margin-bottom: 20px">
          <text style="margin-right: 10px;font-size: 15px;width: 80px">所属课程</text>
          <el-select v-model="options.course_id" style="width: 150px;margin-left: -13px " @change="getMenuList()" placeholder="请选择所属课程">
            <el-option
                v-for="item in course.options"
                :key="item.course_id"
                :label="item.course_name"
                :value="item.course_id" />
          </el-select>
        </div>
        <div style=" display: flex;flex-direction: row" >
          <text style="margin-right: 23px;font-size: 15px;width: 80px">知识点</text>
          <div style="display: flex;flex-direction: column;margin-left: -30px">
            <div style="margin-bottom: 8px" v-for="catalog in catalogs.menuData" >
              <div style=" display: flex;">
                <ArrowDownBold  v-if="catalog.show" style="height: 10px;width: 10px;margin-top: 7px;margin-right: 5px " />
                <ArrowRightBold v-else style="height: 10px;width: 10px;margin-top: 7px;margin-right: 5px "/>
                <span style="cursor: pointer;font-size: 15px" @click="catalogShow(catalog.id)">{{catalog.label}}</span>
              </div>
              <div style="margin-top: 5px">
                <el-radio-group v-if="catalog.show" v-for="item in catalog.children"  style="display: flex;margin-left: 20px;" v-model="options.knowledge_point">
                  <el-radio :label="item.id" style="font-size: 15px">{{ item.label }}</el-radio>
                </el-radio-group>
              </div>
            </div>
          </div>

        </div>
      </div>

      <div v-if="['单选题','多选题'].includes(options.type)" style="width: 400px;">
        <div style="margin-bottom: 10px;display: flex;flex-direction: row;align-items: center">
          <text style="margin-right: 10px;font-size: 15px;width: 20px">A</text>
          <el-input v-model="options.optionsA" placeholder="请输入选项" />
        </div>
        <div style="margin-bottom: 10px;display: flex;flex-direction: row;align-items: center">
          <text style="margin-right: 10px;font-size: 15px;width: 20px">B</text>
          <el-input v-model="options.optionsB" placeholder="请输入选项" />
        </div>
        <div style="margin-bottom: 10px;display: flex;flex-direction: row;align-items: center">
          <text style="margin-right: 10px;font-size: 15px;width: 20px">C</text>
          <el-input  v-model="options.optionsC" placeholder="请输入选项" />
        </div>
        <div  style="margin-bottom: 10px;display: flex;flex-direction: row;align-items: center">
          <text style="margin-right: 10px;font-size: 15px;width: 20px">D</text>
          <el-input  v-model="options.optionsD" placeholder="请输入选项" />
        </div>
      </div>
    </div>
    <el-button v-if="['单选题','多选题'].includes(options.type)" style="position: absolute;left: 45%;" @click="saveQuestion()" type="primary" :icon="FolderAdd">保存</el-button>
    <el-button v-else style="position: absolute;left: 25%;" @click="saveQuestion()" type="primary" :icon="FolderAdd">保存</el-button>
  </el-card>
</template>

<script setup>
import {onMounted, reactive, ref} from 'vue'
import { useRouter } from 'vue-router'
import { Back } from '@element-plus/icons-vue'
import { FolderAdd } from '@element-plus/icons-vue'
import https from "@/apis/axio"
import { ElMessage } from "element-plus"
import Latex from "../components/latex.vue"

let catalogs=reactive({
  menuData:[]
})
const add = (e) => {
  options.question += e
}
const router = useRouter()
const options=reactive({
  type: JSON.parse(localStorage.getItem('question_data')).type,
  id: JSON.parse(localStorage.getItem('question_data')).id,
  question: JSON.parse(localStorage.getItem('question_data')).question,
  optionsA: JSON.parse(localStorage.getItem('question_data')).optionsA,
  optionsB: JSON.parse(localStorage.getItem('question_data')).optionsB,
  optionsC: JSON.parse(localStorage.getItem('question_data')).optionsC,
  optionsD: JSON.parse(localStorage.getItem('question_data')).optionsD,
  answer: JSON.parse(localStorage.getItem('question_data')).answer,
  answers: JSON.parse(localStorage.getItem('question_data')).answers,
  analysis: JSON.parse(localStorage.getItem('question_data')).analysis,
  degree: JSON.parse(localStorage.getItem('question_data')).degree,
  course_id: JSON.parse(localStorage.getItem('question_data')).course_id,
  knowledge_point: JSON.parse(localStorage.getItem('question_data')).knowledge_point
})
const selects=['A','B','C','D']
const degrees = [{value: '简单', label: '简单'}, {value: '普通', label: '普通'}, {value: '困难', label: '困难'}]
const course=reactive({
  options:[]
})

onMounted(()=> {
  https.post('/teacher/get_courses',{'username':JSON.parse(localStorage.getItem('token')).username}).then(res => {
    course.options = res.data
  })
  getMenuList()
})

function back() {
  router.push("/questions")
}

function getMenuList () {
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

function saveQuestion(){
  https.post('/teacher/edit_question', options).then(res=>{
    if (res.data.code === 200){
      ElMessage.success('修改成功')
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
  overflow: auto;
}
.fistBox :hover{
  background-color: #F5F5F5;
}
</style>
