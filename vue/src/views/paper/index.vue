<template>
  <el-row :gutter="75">
    <el-col :span="17" >
      <el-card>
        <template #header>
          <span>试卷管理</span>
          <el-button type="primary" @click="addPaper()">新建试卷</el-button>
        </template>

        <el-table :data="paperData" style="width: 100%;height: 100%;overflow: auto" tooltip-effect="dark" >
          <el-table-column type="index"  label="#" width="50" />
          <el-table-column prop="paper_id" label="试卷编号" width="120" show-overflow-tooltip />
          <el-table-column prop="paper_name" label="试卷名称" width="120" show-overflow-tooltip />
          <el-table-column prop="course_name" label="所属课程" width="150" show-overflow-tooltip />
          <el-table-column prop="catalog_name" label="知识点" width="150" show-overflow-tooltip/>
          <el-table-column label="总分" width="80" >
            <template #default="scope">
              <text>{{ scope.row.paper_score +'分' }}</text>
            </template>
          </el-table-column>
          <el-table-column prop="paper_num" label="题目数量" width="80" align="center"/>
          <el-table-column align="center" label="操作">
            <template #default="scope">
              <PreviewOpen style="margin-right: 10px;cursor: pointer " fill="#333" size="20" @click="paperDetail(scope.row)"/>
              <EditTwo fill="#333" size="20" style="margin-right: 10px;cursor: pointer "  @click="editDialog(scope.row)"/>
              <el-popconfirm
                  title="确定要删除吗？"
                  confirm-button-text="确定"
                  cancel-button-text="取消"
                  @confirm="deletePaper(scope.row)">
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
        <search-paper @search_paper="searchResult" />
      </el-card>
    </el-col>
  </el-row>

  <el-dialog v-model="dialogFormVisible" title="修改试卷信息" draggable width="35%">
    <el-divider style="margin-top: -20px" />
    <el-form :model="paperFormDialog" style="margin-top: -10px" label-width="80px" label-position="left">
      <el-form-item label="试卷代码" >
        <el-input v-model="paperFormDialog.paper_id" placeholder="请输入试卷代码" style="width: 60%"></el-input>
      </el-form-item>
      <el-form-item label="试卷名称" >
        <el-input v-model="paperFormDialog.paper_name" placeholder="请输入试卷名称" style="width: 60%"></el-input>
      </el-form-item>
      <div style="position: absolute;right: 0;margin-top: -15px;margin-right: 20px">
        <el-button @click="editPaper()" type="primary">确 定</el-button>
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
import searchPaper from '../paper/components/searchPaper.vue'

let paperData=ref()
let dialogFormVisible = ref(false)
const router = useRouter()
const paperFormDialog=reactive({
  id:'',
  paper_id:'',
  paper_name:''
})
const searchResult = (value) => {
  paperData.value = value
}
onMounted(()=>{
  getPaper()
})

function getPaper() {
  https.post('/teacher/get_paper',{'teacher':JSON.parse(localStorage.getItem('token')).username}).then(res => {
    res.data.forEach(item=>{
      item.catalog_name=item.catalog_name.join('，')
    })
    paperData.value=res.data
  })
}

function addPaper() {
  router.push({ path: "/add_paper" })
}
function paperDetail(item) {
  router.push({
    name: 'detail_paper',
    query:{
      paper_id:item.id
    }
  })
}

function editDialog(e) {
  dialogFormVisible.value = true
  paperFormDialog.id=e.id
  paperFormDialog.paper_id=e.paper_id
  paperFormDialog.paper_name=e.paper_name
}
function editPaper(e) {
  https.post('/teacher/edit_paper', paperFormDialog).then(res=>{
    if (res.data.code === 200){
      ElMessage.success('修改成功')
      dialogFormVisible.value = false
      getPaper()
    } else {
      ElMessage.error(res.data.message)
    }
  })
}

function deletePaper(e) {
  https.post('/teacher/delete_paper', {'data_id':e.id}).then(res=>{
    if (res.data.code === 200){
      ElMessage.success('删除成功')
      getPaper()
    } else {
      ElMessage.error(res.data.message)
    }
  })
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