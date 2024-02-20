<template>
  <el-row :gutter="75">
    <el-col :span="17" >
      <el-card>
        <template #header>
          <span>我的考试</span>
        </template>

        <el-card v-for="item in examData">
          <div style="display: flex;justify-content: space-between;align-items: center">
            <div>
              <div>
                <text>考试编号：</text>
                <text style="font-weight: bold;">{{ item.exam_id }}</text>
                <text style="margin-left: 20px">考试名称：</text>
                <text style="font-weight: bold;">{{ item.exam_name }}</text>
                <text style="margin-left: 20px;font-size: 13px;background-color: #ADD8E6;padding: 5px 10px;border-radius: 4px">{{ item.situation }}</text>
                <text style="margin-left: 10px;font-size: 13px;background-color: #ADD8E6;padding: 5px 10px;border-radius: 4px">{{ item.exam_type }}</text>
              </div>
              <div style="margin-top: 15px;font-size: 15px">
                <text>考试日期：{{ item.exam_date }}</text>
                <text style="margin-left: 15px">考试时间：{{ item.start_time }} - {{ item.end_time }}</text>
                <text style="margin-left: 15px">总分：{{ item.exam_score }}分</text>
                <text style="margin-left: 15px">所属课程：{{ item.course_name }}</text>
              </div>
            </div>
            <div>
              <text v-if="item.situation==='未开始'">未开始</text>
              <text v-if="item.situation==='已结束'">未参加</text>
              <el-button v-if="item.situation==='进行中'" type="primary"  @click="beginExam(item)">参加考试</el-button>
              <div v-if="item.situation==='已考完'" style="display: flex;flex-flow: column;align-items: flex-end">
                <text style="margin-bottom: 20px">得分：{{ item.score }}分</text>
                <el-button type="primary"  @click="resultDetail(item)">查看详细情况</el-button>
              </div>
            </div>
          </div>

        </el-card>

      </el-card>
    </el-col>

    <el-col :span="7" >
      <el-card>
<!--        <search-exam @search_exam="searchResult" />-->
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup>
import {DeleteFour, EditTwo} from "@icon-park/vue-next";
import {onMounted, ref} from "vue";
import https from "@/apis/axio.js";
import {useRoute, useRouter} from "vue-router";

const route = useRoute()
const router = useRouter()
let examData=ref()
onMounted(()=>{
  getExam()
})
function getExam() {
  https.post('/student/get_exam',{'username':JSON.parse(localStorage.getItem('token')).username}).then(res => {
    examData.value=res.data
  })
}

function beginExam(e) {
  router.push({
    name: 'exam_paper',
    query:{
      exam_id:e.exam_id
    }
  })
}
function resultDetail(e) {
  router.push({
    name: 'detail_exam',
    query:{
      exam_id:e.exam_id
    }
  })
}

</script>

<style scoped lang="scss">
.el-row {
  height: 100%;
  padding-left: 10px;
  padding-top: 10px;
}
.el-card{
  height: 100%;
}
:deep(.el-card__header) {
  background-color: #E6E6FA;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>