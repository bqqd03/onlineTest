<template>
  <div style="display: flex;justify-content: space-between;align-items: center;padding: 20px 30px;background-color: #ADD8E6">
    <text>试卷  {{ examData.paper_id }}</text>
    <text style="margin-left: 20px">考生 {{ examData.student_name }}</text>
    <text style="margin-left: 20px">考试时长 {{ examData.answerTime }}分钟</text>
    <text style="margin-left: 20px">倒计时 {{ hour }}:{{ minute }}:{{ second }}</text>
  </div>

  <div style="margin-left: 20px;margin-top: 10px">
    <el-scrollbar :style="{ height: scrollCardHeight }">
      <div v-if="questions.single.length!==0">
        <text style="font-size: 20px">单选题（共 {{ questions.single.length }} 题，合计 {{ questions.single.length*questions.single[0].score }} 分）</text>
        <el-card v-for="(item,index) in questions.single" style="margin-top: 15px;margin-left: 10px">
          <div style="margin-bottom: 20px">
            <div style="display: flex;align-items: center;">
              <text class="index_box">{{ index+1 }}</text>
              <text>{{ item.question}}（{{ item.score }} 分）</text>
            </div>
            <el-radio-group  style="margin-left: 40px;margin-top: 10px;display: flex;flex-flow: column;align-items: flex-start" v-model="item.studentAnswer" >
              <el-radio label="A">A、{{ item.optionsA }}</el-radio>
              <el-radio label="B">B、{{ item.optionsB }}</el-radio>
              <el-radio label="C">C、{{ item.optionsC }}</el-radio>
              <el-radio label="D">D、{{ item.optionsD }}</el-radio>
            </el-radio-group>
          </div>
        </el-card>
      </div>

      <div v-if="questions.multiple.length!==0" style="margin-top: 20px">
        <text style="font-size: 20px">多选题（共 {{ questions.multiple.length }} 题，合计 {{ questions.multiple.length*questions.multiple[0].score }} 分）</text>
        <el-card v-for="(item,index) in questions.multiple" style="margin-top: 15px;margin-left: 10px">
          <div style="margin-bottom: 20px">
            <div style="display: flex;align-items: center;">
              <text class="index_box">{{ index+1 }}</text>
              <text>{{ item.question}}（{{ item.score }} 分）</text>
            </div>
            <el-checkbox-group v-model="item.studentAnswer" style="margin-left: 40px;display: flex;flex-flow: column;margin-top: 10px">
              <el-checkbox label="A">A、{{ item.optionsA }}</el-checkbox>
              <el-checkbox label="B">B、{{ item.optionsB }}</el-checkbox>
              <el-checkbox label="C">C、{{ item.optionsC }}</el-checkbox>
              <el-checkbox label="D">D、{{ item.optionsD }}</el-checkbox>
            </el-checkbox-group>
          </div>

        </el-card>
      </div>

      <div v-if="questions.judgment.length!==0" style="margin-top: 20px">
        <text style="font-size: 20px">判断题（共 {{ questions.judgment.length }} 题，合计 {{ questions.judgment.length*questions.judgment[0].score }} 分）</text>
        <el-card v-for="(item,index) in questions.judgment" style="margin-top: 15px;margin-left: 10px">
          <div style="margin-bottom: 20px">
            <div style="display: flex;align-items: center;">
              <text class="index_box">{{ index+1 }}</text>
              <text>{{ item.question}}（{{ item.score }} 分）</text>
            </div>
            <el-radio-group  style="margin-left: 40px;margin-top: 10px;display: flex;flex-flow: column;align-items: flex-start"  v-model="item.studentAnswer" >
              <el-radio label="T">T</el-radio>
              <el-radio label="F">F</el-radio>
            </el-radio-group >
          </div>
        </el-card>
      </div>

      <div v-if="questions.blank.length!==0" style="margin-top: 20px">
        <text style="font-size: 20px">填空题（共 {{ questions.blank.length }} 题，合计 {{ questions.blank.length*questions.blank[0].score }} 分）</text>
        <el-card v-for="(item,index) in questions.blank" style="margin-top: 15px;margin-left: 10px">
          <div style="margin-bottom: 20px">
            <div style="display: flex;align-items: center;">
              <text class="index_box">{{ index+1 }}</text>
              <text>{{ item.question}}（{{ item.score }} 分）</text>
            </div>
            <el-input  style="margin-left: 40px;margin-top: 10px;width: 80%" v-model="item.studentAnswer"></el-input>
          </div>
        </el-card>
      </div>

      <div v-if="questions.answer.length!==0" style="margin-top: 20px">
        <text style="font-size: 20px">问答题（共 {{ questions.answer.length }} 题，合计 {{ questions.answer.length*questions.answer[0].score }} 分）</text>
        <el-card v-for="(item,index) in questions.answer" style="margin-top: 15px;margin-left: 10px">
          <div style="margin-bottom: 20px">
            <div style="display: flex;align-items: center;">
              <text class="index_box">{{ index+1 }}</text>
              <text>{{ item.question}}（{{ item.score }} 分）</text>
            </div>
            <el-input rows="3" type="textarea" style="margin-left: 40px;margin-top: 10px;width: 80%" v-model="item.studentAnswer"></el-input>
          </div>
        </el-card>
      </div>
    </el-scrollbar>


    <div style="margin-top: 20px;position: absolute;right: 46%;height: 5%">
      <el-button type="primary"  @click="save()">保存</el-button>
    </div>

  </div>


</template>

<script setup>
import {onMounted, reactive, ref, watch} from "vue"
import https from "@/apis/axio"
import { useRoute,useRouter } from 'vue-router'
import { ElMessage } from "element-plus";
import {Back} from "@element-plus/icons-vue";

const scrollCardHeight = (document.documentElement.clientHeight - 140).toString() + "px"
const route = useRoute()
const router = useRouter()
const questions=reactive({
  single:[],
  multiple:[],
  judgment:[],
  blank:[],
  answer:[]
})
const examData=reactive({
  exam_id:route.query.exam_id,
  paper_id:'',
  student_name:JSON.parse(localStorage.getItem('token')).username,
  answerTime:''
})
const clock=reactive({
  options:0,
  minute:0,
  second:0,
  aa:60
})
let hour=ref()
let minute=ref()
let second=ref()
let timer = setInterval(() => {
  clock.options++
}, examData.answerTime*60000) //定时器

watch(()=>clock.options, (newClock) => {

  let remainder = newClock%1000
  if (remainder===0){
    clock.second++
    second.value= parseInt(60-clock.second).toString().padStart(2, '0')
  }
  if (clock.second===60){
    clock.second=0
    clock.minute++
    clock.aa--
    minute.value= parseInt(clock.aa-1).toString().padStart(2, '0')
  }
  if (clock.minute===60){
    clock.minute=0
    hour.value= parseInt(parseInt(hour.value)-1).toString().padStart(2, '0')
  }
  if (minute.value==='00'){
    clock.aa=60
  }
  if (hour.value==='00'&&minute.value==='00'&&second.value==='00'){
    clearInterval(timer)
    save()
  }
})


onMounted(()=>{
  https.post('/student/exam_paper',{'exam_id':route.query.exam_id}).then(res => {
    questions.single=res.data.paperData['单选题']
    questions.multiple=res.data.paperData['多选题']
    questions.judgment=res.data.paperData['判断题']
    questions.blank=res.data.paperData['填空题']
    questions.answer=res.data.paperData['问答题']
    examData.paper_id =res.data.examData.exam_paper
    examData.answerTime =res.data.examData.answer_time
    hour.value= parseInt(parseInt(examData.answerTime)/60).toString().padStart(2, '0')
    minute.value= (parseInt(parseInt(examData.answerTime)-parseInt(hour.value)*60)).toString().padStart(2, '0')
    if (minute.value==='00'){
      minute.value='59'
      hour.value=parseInt(parseInt(hour.value)-1).toString().padStart(2, '0')
    }
    second.value= '59'
  })
})


function save() {
  https.post('/student/save_exam',{'question':questions,'examData':examData}).then(res => {
    if (res.data.code===200){
      ElMessage.success('考试结束')
      router.push('/student_exam')
    }
  })
}

</script>

<style scoped lang="scss">
.index_box{
  background: #409eff;
  padding: 5px 10px;
  color: #f2f2f2;
  border-radius: 5px;
  margin-right: 10px;
}
.content{
  background: bisque;
  font-size: 15px;
  border: 1px #ddd solid;
  padding: 3px 10px;
  border-radius: 3px;
  text-align: center;
  margin-left: 25px;
  margin-top: 5px;
}
.answer_box{
  border-radius: 50%;
  border: 1px solid #666;
  padding: 3px 9px;
  margin-right: 10px;
}
</style>