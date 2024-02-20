<template>
  <div style="display: flex;justify-content: space-between;align-items: center;padding: 20px 30px;background-color: #ADD8E6">
    <text>考试编号：{{ questions.userInfo.exam_id }}</text>
    <text style="margin-left: 20px">考生姓名：{{ questions.userInfo.student_name }}</text>
    <text style="margin-left: 20px">分数：{{ questions.userInfo.score }}分</text>
    <text style="margin-left: 20px">提交时间：{{ questions.userInfo.submissionTime }}</text>
  </div>


  <div style="margin-left: 20px;margin-top: 10px">
    <el-scrollbar :style="{ height: scrollCardHeight }">
      <div v-if="questions.single.length!==0">
        <text style="font-size: 20px">单选题（共 {{ questions.single.length }} 题，合计 {{ questions.single.length*questions.single[0].score }} 分）</text>
        <el-card v-for="(item,index) in questions.single" style="margin-top: 15px;margin-left: 10px;">
          <div style="display: flex;justify-content: space-between;">
            <div style="margin-bottom: 20px;">
              <div style="display: flex;align-items: center;">
                <text class="index_box">{{ index+1 }}</text>
                <text>{{ item.question}}（{{ item.score }} 分）</text>
              </div>
              <div style="margin-left: 50px;display: flex;flex-flow: column;margin-top: 10px" >
                <el-radio label="A" :model-value=item.studentAnswer>A、{{ item.optionsA }}</el-radio>
                <el-radio label="B" :model-value=item.studentAnswer>B、{{ item.optionsB }}</el-radio>
                <el-radio label="C" :model-value=item.studentAnswer>C、{{ item.optionsC }}</el-radio>
                <el-radio label="D" :model-value=item.studentAnswer>D、{{ item.optionsD }}</el-radio>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">考试答案</span>
                <span style="font-size: 18px">{{ item.studentAnswer}}</span>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">正确答案</span>
                <span style="font-size: 18px">{{ item.answer}}</span>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">答案解析</span>
                <span style="font-size: 13px">{{ item.analysis }}</span>
              </div>
            </div>
            <div>
              <div v-if="item.status==='success'">
                <text style="padding:10px;background-color: forestgreen;color: #f2f2f2;border: 1px solid forestgreen;border-radius: 10% 0 0 10% ">正确</text>
                <text style="padding:10px;border: 1px solid #666666;border-radius: 0 10% 10% 0">错误</text>
              </div>
              <div v-if="item.status==='error'">
                <text style="padding:10px;border: 1px solid #666666;border-radius: 10% 0 0 10% ">正确</text>
                <text style="background-color: crimson;color: #f2f2f2;padding:10px;border: 1px solid crimson;border-radius: 0 10% 10% 0">错误</text>
              </div>
            </div>
          </div>


        </el-card>
      </div>

      <div v-if="questions.multiple.length!==0" style="margin-top: 20px">
        <text style="font-size: 20px">多选题（共 {{ questions.multiple.length }} 题，合计 {{ questions.multiple.length*questions.multiple[0].score }} 分）</text>
        <el-card v-for="(item,index) in questions.multiple" style="margin-top: 15px;margin-left: 10px">
          <div style="display: flex;justify-content: space-between;">
            <div style="margin-bottom: 20px">
              <div style="display: flex;align-items: center;">
                <text class="index_box">{{ index+1 }}</text>
                <text>{{ item.question}}（{{ item.score }} 分）</text>
              </div>
              <el-checkbox-group  :model-value="item.studentAnswers" style="margin-left: 50px;display: flex;flex-flow: column;margin-top: 10px">
                <el-checkbox label="A">A、{{ item.optionsA }}</el-checkbox>
                <el-checkbox label="B">B、{{ item.optionsB }}</el-checkbox>
                <el-checkbox label="C">C、{{ item.optionsC }}</el-checkbox>
                <el-checkbox label="D">D、{{ item.optionsD }}</el-checkbox>
              </el-checkbox-group>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">考试答案</span>
                <span style="font-size: 18px">{{ item.studentAnswer}}</span>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">正确答案</span>
                <span style="font-size: 18px">{{ item. answer}}</span>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">答案解析</span>
                <span style="font-size: 13px">{{ item.analysis }}</span>
              </div>
            </div>
            <div>
              <div v-if="item.status==='success'">
                <text style="padding:10px;background-color: forestgreen;color: #f2f2f2;border: 1px solid forestgreen;border-radius: 10% 0 0 10% ">正确</text>
                <text style="padding:10px;border: 1px solid #666666;border-radius: 0 10% 10% 0">错误</text>
              </div>
              <div v-if="item.status==='error'">
                <text style="padding:10px;border: 1px solid #666666;border-radius: 10% 0 0 10% ">正确</text>
                <text style="background-color: crimson;color: #f2f2f2;padding:10px;border: 1px solid crimson;border-radius: 0 10% 10% 0">错误</text>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <div v-if="questions.judgment.length!==0" style="margin-top: 20px">
        <text style="font-size: 20px">判断题（共 {{ questions.judgment.length }} 题，合计 {{ questions.judgment.length*questions.judgment[0].score }} 分）</text>
        <el-card v-for="(item,index) in questions.judgment" style="margin-top: 15px;margin-left: 10px">
          <div style="display: flex;justify-content: space-between;">
            <div style="margin-bottom: 20px">
              <div style="display: flex;align-items: center;">
                <text class="index_box">{{ index+1 }}</text>
                <text>{{ item.question}}（{{ item.score }} 分）</text>
              </div>
              <div style="margin-left: 50px;display: flex;flex-flow: column;margin-top: 10px" >
                <el-radio label="T" :model-value=item.answer>T</el-radio>
                <el-radio label="F" :model-value=item.answer>F</el-radio>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">考试答案</span>
                <span style="font-size: 18px">{{ item.studentAnswer}}</span>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">正确答案</span>
                <span style="font-size: 18px">{{ item. answer}}</span>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">答案解析</span>
                <span style="font-size: 13px">{{ item.analysis }}</span>
              </div>
            </div>
            <div>
              <div v-if="item.status==='success'">
                <text style="padding:10px;background-color: forestgreen;color: #f2f2f2;border: 1px solid forestgreen;border-radius: 10% 0 0 10% ">正确</text>
                <text style="padding:10px;border: 1px solid #666666;border-radius: 0 10% 10% 0">错误</text>
              </div>
              <div v-if="item.status==='error'">
                <text style="padding:10px;border: 1px solid #666666;border-radius: 10% 0 0 10% ">正确</text>
                <text style="background-color: crimson;color: #f2f2f2;padding:10px;border: 1px solid crimson;border-radius: 0 10% 10% 0">错误</text>
              </div>
            </div>
          </div>

        </el-card>
      </div>

      <div v-if="questions.blank.length!==0" style="margin-top: 20px">
        <text style="font-size: 20px">填空题（共 {{ questions.blank.length }} 题，合计 {{ questions.blank.length*questions.blank[0].score }} 分）</text>
        <el-card v-for="(item,index) in questions.blank" style="margin-top: 15px;margin-left: 10px">
          <div style="display: flex;justify-content: space-between;">
            <div style="margin-bottom: 20px">
              <div style="display: flex;align-items: center;">
                <text class="index_box">{{ index+1 }}</text>
                <text>{{ item.question}}（{{ item.score }} 分）</text>
              </div>
              <div style="display: flex;margin-top: 20px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">考试答案</span>
                <span style="font-size: 18px">{{ item.studentAnswer}}</span>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">正确答案</span>
                <span style="font-size: 18px">{{ item. answer}}</span>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">答案解析</span>
                <span style="font-size: 13px">{{ item.analysis }}</span>
              </div>
            </div>
            <div>
              <div v-if="item.status==='success'">
                <text style="padding:10px;background-color: forestgreen;color: #f2f2f2;border: 1px solid forestgreen;border-radius: 10% 0 0 10% ">正确</text>
                <text style="padding:10px;border: 1px solid #666666;border-radius: 0 10% 10% 0">错误</text>
              </div>
              <div v-if="item.status==='error'">
                <text style="padding:10px;border: 1px solid #666666;border-radius: 10% 0 0 10% ">正确</text>
                <text style="background-color: crimson;color: #f2f2f2;padding:10px;border: 1px solid crimson;border-radius: 0 10% 10% 0">错误</text>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <div v-if="questions.answer.length!==0" style="margin-top: 20px">
        <text style="font-size: 20px">问答题（共 {{ questions.answer.length }} 题，合计 {{ questions.answer.length*questions.answer[0].score }} 分）</text>
        <el-card v-for="(item,index) in questions.answer" style="margin-top: 15px;margin-left: 10px">
          <div style="display: flex;justify-content: space-between;">
            <div style="margin-bottom: 20px">
              <div style="display: flex;align-items: center;">
                <text class="index_box">{{ index+1 }}</text>
                <text>{{ item.question}}（{{ item.score }} 分）</text>
              </div>
              <div style="display: flex;margin-top: 20px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">考试答案</span>
                <span style="font-size: 18px">{{ item.studentAnswer}}</span>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">正确答案</span>
                <span style="font-size: 18px">{{ item. answer}}</span>
              </div>
              <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
                <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">答案解析</span>
                <span style="font-size: 13px">{{ item.analysis }}</span>
              </div>
            </div>
            <div>
              <div v-if="item.status==='success'">
                <text style="padding:10px;background-color: forestgreen;color: #f2f2f2;border: 1px solid forestgreen;border-radius: 10% 0 0 10% ">正确</text>
                <text style="padding:10px;border: 1px solid #666666;border-radius: 0 10% 10% 0">错误</text>
              </div>
              <div v-if="item.status==='error'">
                <text style="padding:10px;border: 1px solid #666666;border-radius: 10% 0 0 10% ">正确</text>
                <text style="background-color: crimson;color: #f2f2f2;padding:10px;border: 1px solid crimson;border-radius: 0 10% 10% 0">错误</text>
              </div>
            </div>
          </div>

        </el-card>
      </div>
    </el-scrollbar>

    <div style="margin-top: 20px;position: absolute;right: 48%;height: 5%">
      <el-button  type="info" :icon="Back" @click="back()">返回</el-button>
    </div>

  </div>


</template>

<script setup>
import {onMounted, reactive, ref} from "vue"
import https from "@/apis/axio"
import { useRoute,useRouter } from 'vue-router'
import { ElMessage } from "element-plus";
import {Back} from "@element-plus/icons-vue";

const scrollCardHeight = (document.documentElement.clientHeight - 140).toString() + "px"
const role = JSON.parse(localStorage.getItem('token')).role
const route = useRoute()
const router = useRouter()
const questions=reactive({
  single:[],
  multiple:[],
  judgment:[],
  blank:[],
  answer:[],
  userInfo:[]
})

onMounted(()=>{
  https.post('/student/exam_detail',{'exam_id':route.query.exam_id,'username':JSON.parse(localStorage.getItem('token')).username}).then(res => {
    questions.single=res.data['单选题']
    questions.multiple=res.data['多选题']
    questions.judgment=res.data['判断题']
    questions.blank=res.data['填空题']
    questions.answer=res.data['问答题']
    questions.userInfo=res.data['考试信息']
  })
})

function back() {
  if (role==='student'){
    router.push("/student_exam")
  }

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
</style>