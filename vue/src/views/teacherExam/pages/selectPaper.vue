<template>
  <el-card style="height: 18%;width: 80%;position: relative;left: 9.5%" >
    <template #header>
      <span>考试信息</span>
    </template>
    <div style="display: flex;justify-content: space-between;">
      <text class="item_box">考试代码：{{ examInfo.exam_id }}</text>
      <text class="item_box">考试名称：{{ examInfo.exam_name }}</text>
      <text class="item_box">选择课程：{{ examInfo.exam_course }}</text>
      <text class="item_box">考试类型：{{ examInfo.exam_type }}</text>
    </div>

  </el-card>
  <el-card style="height: 78%;width: 80%;position: relative;left: 9.5%;top: 3%;overflow: auto" >
    <template #header>
      <span>试卷</span>
    </template>
    <el-card style="margin-bottom: 30px" v-for="item in examInfo.paper">
      <div style="display: flex;justify-content: space-between;align-items: center">
        <div>
          <div>
            <text>{{ item.paper_name }}</text>
            <text style="margin-left: 25px;font-size: 13px;background-color: #ADD8E6;padding: 5px 10px">{{ examInfo.exam_course }}</text>
          </div>
          <div style="margin-top: 12px">
            <text>总分：{{ item.paper_score }}分</text>
            <text style="margin-left: 20px">试卷编号：{{ item.paper_id }}</text>
          </div>
        </div>
        <div>
          <el-button type="primary"  @click="selectPaper(item)">选择</el-button>
        </div>
      </div>
    </el-card>

  </el-card>
</template>

<script setup>
import {onMounted, reactive,ref} from "vue";
import https from "@/apis/axio.js";
import {useRoute, useRouter} from "vue-router";
import {ElMessage} from "element-plus";

const route = useRoute()
const router = useRouter()
let  examInfo = reactive({
  exam_id:'',
  exam_name:'',
  exam_course:'',
  exam_type:'',
  paper:[]
})
let paper=ref()

onMounted(()=> {
  https.post('/teacher/exam_info',{'exam_id':route.query.exam_id}).then(res => {
    examInfo.exam_id = res.data.exam_id
    examInfo.exam_name = res.data.exam_name
    examInfo.exam_course = res.data.exam_course
    examInfo.exam_type = res.data.exam_type
    examInfo.paper=res.data.paper
  })
})

function selectPaper(item) {
  https.post('/teacher/exam_paper',{'exam_id':route.query.exam_id,'exam_paper':item.paper_id,'exam_score':item.paper_score}).then(res => {
    if (res.data.code===200){
      ElMessage.success('添加成功')
      router.push('/teacher_exam')
    }
  })
}

</script>

<style scoped lang="scss">
.item_box{
  font-size: 18px;
  margin-left: 20px;
  margin-right: 20px;
}
</style>