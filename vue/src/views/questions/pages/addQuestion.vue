<template>
  <div class="card-header">
    <span>添加题目</span>
    <el-button type="info" :icon="Back" @click="back">返回</el-button>
  </div>
  <div style="display: flex; margin-top: 3px;">
    <span>题型</span>
    <el-radio-group v-model="options.type" style="margin: -3px 0 5px 10px;" >
      <el-radio-button label="单选题"/>
      <el-radio-button label="多选题"/>
      <el-radio-button label="判断题"/>
      <el-radio-button label="填空题"/>
      <el-radio-button label="问答题"/>
    </el-radio-group>
  </div>
  <el-card >
    <template #header>
      <div style="font-size: 20px;display: flex;justify-content: space-between">
        <span>添加{{ options.type }}</span>
        <el-button  @click="saveQuestion()" type="primary" :icon="FolderAdd">保存</el-button>
      </div>
    </template>
    <div style="margin-top: 5px;display: flex;justify-content: space-between;margin-bottom: 20px;width: 1000px">
      <div style=" display: flex;flex-direction: column;width: 500px">
        <div style=" display: flex;flex-direction: row;margin-bottom: 20px">
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
            <el-select  v-model="options.degree" style="width: 130px;margin-left: -13px">
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
        <div style="display: flex;flex-direction: row;align-items: center;margin-bottom: 20px">
          <text style="margin-right: 10px;font-size: 15px;width: 80px">所属课程</text>
          <el-select v-model="options.course_id" style="width: 150px;margin-left: -13px" @change="getMenuList()" placeholder="请选择所属课程">
            <el-option
                v-for="item in course.options"
                :key="item.course_id"
                :label="item.course_name"
                :value="item.course_id" />
          </el-select>
        </div>
        <div style=" display: flex;flex-direction: row"  v-if="catalogs.showTree">
          <text style="margin-right: 23px;font-size: 15px;width: 80px">知识点</text>
          <div style="display: flex;flex-direction: column;margin-left: -30px">
            <div style="margin-bottom: 8px" v-for="catalog in catalogs.menuData" >
              <div style="display: flex;">
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

      <div v-if="['单选题','多选题'].includes(options.type)" style="width: 400px">
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
          <el-input v-model="options.optionsC" placeholder="请输入选项" />
        </div>
        <div style="display: flex;flex-direction: row;align-items: center">
          <text style="margin-right: 10px;font-size: 15px;width: 20px">D</text>
          <el-input v-model="options.optionsD" placeholder="请输入选项" />
        </div>
      </div>
    </div>
  </el-card>


</template>

<script setup>
import {onMounted, reactive, ref} from 'vue'
import { useRouter } from 'vue-router'
import { Back } from '@element-plus/icons-vue'
import { FolderAdd } from '@element-plus/icons-vue'
import https from "@/apis/axio.js"
import { ElMessage } from "element-plus"
import {DeleteFour, EditTwo, Plus} from "@icon-park/vue-next";

let catalogs=reactive({
  showTree: false,
  menuData:[]
})
const router = useRouter()
const options = reactive({
  type:'单选题',
  question: '',
  optionsA: '',
  optionsB: '',
  optionsC: '',
  optionsD: '',
  answer: '',
  answers:[],
  analysis: '',
  degree: '简单',
  course_id: '',
  knowledge_point: ''
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
})

function back() {
  router.push("/questions")
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
function saveQuestion(){
  https.post('/teacher/add_question', options).then(res=>{
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
  margin-bottom: 20px;
}
.el-card{
  height: 85%;
  overflow: auto;
  margin-top: 10px;
  margin-left: -1px;
}
</style>
