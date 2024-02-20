<template>
  <div class="card-header">
    <span>添加考试</span>
    <el-button type="info" :icon="Back" @click="back">返回</el-button>
  </div>
  <el-card style="height: 290px;" >
    <template #header>
      <span>概要</span>
    </template>

    <div style=" display: flex;flex-direction: row;">
      <div class="item_box">
        <text style="margin-right: -14px;font-size: 15px;width: 85px">考试代码</text>
        <el-input style="width: 220px;" onkeypress='return( /[\d]/.test(String.fromCharCode(event.keyCode)))' v-model="options.exam_id" placeholder="请输入考试代码" />
      </div>

      <div class="item_box">
        <text style="margin-right: -14px;font-size: 15px;width: 85px">考试名称</text>
        <el-input style="width: 220px;" v-model="options.exam_name" placeholder="请输入考试名称" />
      </div>

      <div class="item_box">
        <text style="margin-right: 10px;font-size: 15px;width: 80px">考试类型</text>
        <el-select  v-model="options.exam_type"  style="width: 220px;margin-left: -19px" placeholder="请选择考试类型">
          <el-option
              v-for="item in exam_type"
              :label="item.label"
              :value="item.label" />
        </el-select>
      </div>
    </div>

    <div style=" display: flex;flex-direction: row;margin-top: 15px">
      <div class="item_box">
        <text style="margin-right: 10px;font-size: 15px;width: 80px">所属课程</text>
        <el-select v-model="options.exam_course" style="width: 220px;margin-left: -19px" placeholder="请选择所属课程" @change="getClass()">
          <el-option
              v-for="item in course.options"
              :key="item.course_id"
              :label="item.course_name"
              :value="item.course_id" />
        </el-select>
      </div>
      <div class="item_box" v-if="classes.showTree">
        <text style="margin-right: 10px;font-size: 15px;width: 80px">考试班级</text>
        <el-select v-model="options.exam_class" style="width: 220px;margin-left: -19px" placeholder="请选择所属班级">
          <el-option
              v-for="item in classes.menuData"
              :label="item.class_name"
              :value="item.class_code" />
        </el-select>
      </div>
    </div>
    <div class="item_box" style="margin-top: 20px;">
      <text style="margin-right: -8px;font-size: 15px;width: 80px">注意事项</text>
      <el-input v-model="options.attention" placeholder="请输入注意事项" rows="3" type="textarea" style="width: 530px" />
    </div>
  </el-card>

  <el-card style="height: 190px;margin-top: 20px;" >
    <template #header>
      <span>时间安排</span>
    </template>

    <div style=" display: flex;flex-direction: row">
      <div class="item_box">
        <text style="margin-right: 10px;font-size: 15px;width: 80px">考试日期</text>
        <el-config-provider :locale="locale">
          <el-date-picker
              style="width: 210px;margin-left: -19px"
              v-model="options.exam_date"
              placeholder="选择考试日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              :disabledDate="start_limit"
              :locale="locale"/>
        </el-config-provider>
      </div>
      <div class="item_box">
        <text style="margin-right: 10px;font-size: 15px;width: 80px">答题时间</text>
        <el-input-number
            style="width: 53px;margin-left: -19px"
            v-model="options.answer_time"
            :min="60"
            :max="180"
            :controls="false"/>
        <text style="margin-left: 5px">分钟</text>
      </div>
    </div>
    <div style=" display: flex;flex-direction: row;margin-top: 15px">
      <div class="item_box">
        <text style="margin-right: 10px;font-size: 15px;width: 80px">考试时间</text>
        <el-config-provider :locale="locale">
          <el-time-picker
              style="width: 350px;margin-left: -19px"
              @change="aaa"
              v-model="rangeTime"
              is-range
              range-separator="到"
              format = 'HH:mm'
              value-format = 'HH:mm'
              start-placeholder="选择开始时间"
              end-placeholder="选择结束时间"/>
        </el-config-provider>
      </div>
    </div>
  </el-card>

  <el-button @click="saveExam()" type="primary"  style="position: absolute;left: 50%;right:50%;margin-top: 20px;width: 80px">下一步</el-button>
</template>

<script setup>
import {onMounted, reactive,ref} from 'vue'
import { useRouter } from 'vue-router'
import { Back } from '@element-plus/icons-vue'
import { FolderAdd } from '@element-plus/icons-vue'
import https from "@/apis/axio"
import { ElMessage } from "element-plus"
import zhCn from "element-plus/es/locale/lang/zh-cn"

let locale=zhCn
let rangeTime=ref()
let classes=reactive({
  showTree: false,
  menuData:[]
})

const router = useRouter()
const options=reactive({
  exam_id:'',
  exam_name:'',
  exam_course:'',
  exam_class:'',
  exam_type:'随堂练习',
  exam_date:'',
  start_time:'',
  end_time:'',
  answer_time:60,
  attention:''
})

const course=reactive({
  options:[]
})
const exam_type=[{'label':'随堂练习'},{'label':'期中考试'},{'label':'期末考试'}]


onMounted(()=> {
  https.post('/teacher/get_courses',{'username':JSON.parse(localStorage.getItem('token')).username}).then(res => {
    course.options = res.data
  })
})

function start_limit(time) { // 禁用今天之前的时间
  return time.getTime() < new Date() - 8.64e7
}

function aaa() {
  options.start_time=rangeTime.value[0]
  options.end_time=rangeTime.value[1]
}

function back() {
  router.push("/teacher_exam")
}

function getClass() {
  classes.showTree = true
  options.exam_class=''
  https.post('/teacher/get_class',{'course_id':options.exam_course}).then(res => {
    classes.menuData = res.data
  })
}

function saveExam(){
  https.post('/teacher/add_exam',options).then(res => {
    if (res.data.code===200){
      router.push({
        name: 'select_paper',
        query:{
          exam_id:options.exam_id
        }
      })
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
  margin-bottom: 20px;
}
.item_box{
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-left: 20px;
}

</style>
