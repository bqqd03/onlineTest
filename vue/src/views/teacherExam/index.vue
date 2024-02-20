<template>
  <el-row :gutter="75">
    <el-col :span="17" >
      <el-card>
        <template #header>
          <span>考试管理</span>
          <el-button type="primary" @click="addExam()">新建考试</el-button>
        </template>

        <el-table :data="examData" style="width: 100%;height: 100%;overflow: auto" tooltip-effect="dark" >
          <el-table-column type="index"  label="#" width="50" />
          <el-table-column prop="exam_id" label="考试编号" width="120" show-overflow-tooltip />
          <el-table-column prop="exam_name" label="试卷名称" width="120" show-overflow-tooltip />
          <el-table-column prop="course_name" label="所属课程" width="120" show-overflow-tooltip />
          <el-table-column prop="exam_date" label="考试日期" width="120" show-overflow-tooltip/>
          <el-table-column prop="exam_type" label="考试类别" width="120" show-overflow-tooltip/>
          <el-table-column prop="situation" label="考试状态" width="100" show-overflow-tooltip/>
          <el-table-column label="总分" width="80" >
            <template #default="scope">
              <text>{{ scope.row.exam_score +'分' }}</text>
            </template>
          </el-table-column>
          <el-table-column align="center" label="操作">
            <template #default="scope">
              <EditTwo fill="#333" size="20" style="margin-right: 10px;cursor: pointer "  @click="editDialog(scope.row)"/>
              <el-popconfirm
                  title="确定要删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="取消"
                  @confirm="deleteExam(scope.row)">
                <template #reference>
                  <DeleteFour  fill="#333" size="20" style="cursor: pointer"  />
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-col>

    <el-col :span="7" >
      <el-card>
        <search-exam @search_exam="searchResult" />
      </el-card>
    </el-col>
  </el-row>

  <el-dialog v-model="dialogFormVisible" title="修改考试信息" draggable width="35%" style="height: 52%">
    <el-divider style="margin-top: -20px" />
    <el-form :model="examFormDialog" style="margin-top: -10px" label-width="80px" label-position="left">
      <div style="display: flex;justify-content: space-between;width: 100%">
        <el-form-item label="考试代码" >
          <el-input v-model="examFormDialog.exam_id" placeholder="请输入考试代码" style="width: 85%"></el-input>
        </el-form-item>
        <el-form-item label="考试名称" >
          <el-input v-model="examFormDialog.exam_name" placeholder="请输入考试名称" style="width: 85%"></el-input>
        </el-form-item>
      </div>
      <el-form-item label="考试日期" >
        <el-date-picker
            style="width: 35%"
            v-model="examFormDialog.exam_date"
            placeholder="选择考试日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            :disabledDate="start_limit"
            :locale="locale"/>
      </el-form-item>

      <el-form-item label="考试班级"  >
        <el-select v-model="examFormDialog.exam_class" style="width: 35%" placeholder="请选择考试班级">
          <el-option
              v-for="item in classes.menuData"
              :label="item.class_name"
              :value="item.class_code" />
        </el-select>
      </el-form-item>
      <el-form-item label="答题时间" >
        <el-input-number
            style="width: 27%"
            v-model="examFormDialog.answer_time"
            :min="60"
            :max="180"
            :controls="false"/>
        <text style="margin-left: 5px">分钟</text>
      </el-form-item>


      <div style="display: flex;justify-content: space-between;width: 100%">
        <el-form-item label="开始时间" >
          <el-time-picker
              style="width: 85%"
              v-model="examFormDialog.start_time"
              format = 'HH:mm'
              value-format = 'HH:mm'
              placeholder="选择开始时间"/>
        </el-form-item>
        <el-form-item label="结束时间" >
          <el-time-picker
              style="width: 85%"
              v-model="examFormDialog.end_time"
              format = 'HH:mm'
              value-format = 'HH:mm'
              placeholder="选择结束时间"/>
        </el-form-item>
      </div>

      <div style="position: absolute;right: 0;margin-right: 20px">
        <el-button @click="editExam()" type="primary">确 定</el-button>
        <el-button @click="dialogFormVisible = false">取 消</el-button>
      </div>
    </el-form>
  </el-dialog>

</template>

<script setup>
import {onMounted, reactive, ref} from "vue"
import https from "@/apis/axio"
import { useRouter } from 'vue-router'
import {ElMessage} from "element-plus"
import {DeleteFour, EditTwo, PreviewOpen} from "@icon-park/vue-next"
import searchExam from '../teacherExam/components/searchExam.vue'
import zhCn from "element-plus/es/locale/lang/zh-cn"

let locale=zhCn
let examData=ref()
let dialogFormVisible = ref(false)
const router = useRouter()
const examFormDialog=reactive({
  id:'',
  exam_id:'',
  exam_name:'',
  exam_date:'',
  exam_class:'',
  start_time:'',
  end_time:'',
  answer_time:''
})
let classes=reactive({
  menuData:[]
})


const searchResult = (value) => {
  examData.value = value
}
onMounted(()=>{
  getExam()
})

function getExam() {
  https.post('/teacher/get_exam',{'teacher':JSON.parse(localStorage.getItem('token')).username}).then(res => {
    examData.value=res.data
  })
}

function addExam() {
  router.push("/add_exam")
}
function editDialog(e) {
  dialogFormVisible.value = true
  examFormDialog.id=e.id
  examFormDialog.exam_id=e.exam_id
  examFormDialog.exam_name=e.exam_name
  examFormDialog.exam_date=e.exam_date
  examFormDialog.exam_class=e.exam_class
  examFormDialog.start_time=e.start_time
  examFormDialog.end_time=e.end_time
  examFormDialog.answer_time=e.answer_time
  https.post('/teacher/get_class',{'course_id':e.exam_course}).then(res => {
    classes.menuData = res.data
  })
}
function editExam() {
  https.post('/teacher/edit_exam', examFormDialog).then(res=>{
    if (res.data.code === 200){
      ElMessage.success('修改成功')
      dialogFormVisible.value = false
      getExam()
    } else {
      ElMessage.error(res.data.message)
    }
  })
}

function deleteExam(e) {
  https.post('/teacher/delete_exam', {'data_id':e.id}).then(res=>{
    if (res.data.code === 200){
      ElMessage.success('删除成功')
      getExam()
    } else {
      ElMessage.error(res.data.message)
    }
  })
}

function start_limit(time) { // 禁用今天之前的时间
  return time.getTime() < new Date() - 8.64e7
}
</script>

<style lang="scss" scoped>
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