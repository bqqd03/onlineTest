<template>
  <div style="margin: 40px;overflow: auto">
    <div v-if="questions.single.length!==0">
      <text style="font-size: 20px">单选题（共 {{ questions.single.length }} 题，合计 {{ questions.single.length*questions.single[0].score }} 分）</text>
      <el-card v-for="(item,index) in questions.single" style="margin-top: 15px;margin-left: 10px">
        <div style="margin-bottom: 20px">
          <div style="display: flex;align-items: center;">
            <text class="index_box">{{ index+1 }}</text>
            <text>{{ item.question}}（{{ item.score }} 分）</text>
            <span class="content">{{ item.knowledge_label }}</span>
          </div>
          <div style="margin-left: 50px;display: flex;flex-flow: column;margin-top: 10px" >
            <el-radio label="A" :model-value=item.answer>A、{{ item.optionsA }}</el-radio>
            <el-radio label="B" :model-value=item.answer>B、{{ item.optionsB }}</el-radio>
            <el-radio label="C" :model-value=item.answer>C、{{ item.optionsC }}</el-radio>
            <el-radio label="D" :model-value=item.answer>D、{{ item.optionsD }}</el-radio>
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

      </el-card>
    </div>

    <div v-if="questions.multiple.length!==0" style="margin-top: 20px">
      <text style="font-size: 20px">多选题（共 {{ questions.multiple.length }} 题，合计 {{ questions.multiple.length*questions.multiple[0].score }} 分）</text>
      <el-card v-for="(item,index) in questions.multiple" style="margin-top: 15px;margin-left: 10px">
        <div style="margin-bottom: 20px">
          <div style="display: flex;align-items: center;">
            <text class="index_box">{{ index+1 }}</text>
            <text>{{ item.question}}（{{ item.score }} 分）</text>
            <span class="content">{{ item.knowledge_label }}</span>
          </div>
          <el-checkbox-group  :model-value="item.answers" style="margin-left: 50px;display: flex;flex-flow: column;margin-top: 10px">
            <el-checkbox label="A">A、{{ item.optionsA }}</el-checkbox>
            <el-checkbox label="B">B、{{ item.optionsB }}</el-checkbox>
            <el-checkbox label="C">C、{{ item.optionsC }}</el-checkbox>
            <el-checkbox label="D">D、{{ item.optionsD }}</el-checkbox>
          </el-checkbox-group>
          <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
            <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">正确答案</span>
            <span style="font-size: 18px">{{ item. answer}}</span>
          </div>
          <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
            <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">答案解析</span>
            <span style="font-size: 13px">{{ item.analysis }}</span>
          </div>
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
            <span class="content">{{ item.knowledge_label }}</span>
          </div>
          <div style="margin-left: 50px;display: flex;flex-flow: column;margin-top: 10px" >
            <el-radio label="T" :model-value=item.answer>T</el-radio>
            <el-radio label="F" :model-value=item.answer>F</el-radio>
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
      </el-card>
    </div>

    <div v-if="questions.blank.length!==0" style="margin-top: 20px">
      <text style="font-size: 20px">填空题（共 {{ questions.blank.length }} 题，合计 {{ questions.blank.length*questions.blank[0].score }} 分）</text>
      <el-card v-for="(item,index) in questions.blank" style="margin-top: 15px;margin-left: 10px">
        <div style="margin-bottom: 20px">
          <div style="display: flex;align-items: center;">
            <text class="index_box">{{ index+1 }}</text>
            <text>{{ item.question}}（{{ item.score }} 分）</text>
            <span class="content">{{ item.knowledge_label }}</span>
          </div>
          <div style="display: flex;margin-top: 20px;margin-left: 50px;align-items: center;flex-direction: row;">
            <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">正确答案</span>
            <span style="font-size: 18px">{{ item. answer}}</span>
          </div>
          <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
            <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">答案解析</span>
            <span style="font-size: 13px">{{ item.analysis }}</span>
          </div>
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
            <span class="content">{{ item.knowledge_label }}</span>
          </div>
          <div style="display: flex;margin-top: 20px;margin-left: 50px;align-items: center;flex-direction: row;">
            <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">正确答案</span>
            <span style="font-size: 18px">{{ item. answer}}</span>
          </div>
          <div style="display: flex;margin-top: 5px;margin-left: 50px;align-items: center;flex-direction: row;">
            <span style="font-weight: bolder;font-size: 16px;margin-right: 10px">答案解析</span>
            <span style="font-size: 13px">{{ item.analysis }}</span>
          </div>
        </div>
      </el-card>
    </div>
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


const route = useRoute()
const router = useRouter()
const questions=reactive({
  single:[],
  multiple:[],
  judgment:[],
  blank:[],
  answer:[]
})

onMounted(()=>{
  https.post('/teacher/paper_detail',{'paper_id':route.query.paper_id}).then(res => {
    questions.single=res.data['单选题']
    questions.multiple=res.data['多选题']
    questions.judgment=res.data['判断题']
    questions.blank=res.data['填空题']
    questions.answer=res.data['问答题']
  })
})

function back() {
  router.push("/paper")
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