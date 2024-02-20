<template>
  <span class="search_title">试卷搜索</span>
  <el-form class="searchForm">
    <el-form-item label="试卷代码">
      <el-input style="width: 83%" v-model="searchForm.paper_id" placeholder="请输入试卷代码"/>
    </el-form-item>
    <el-form-item label="试卷名称">
      <el-input style="width: 83%" v-model="searchForm.paper_name" placeholder="请输入试卷名称"/>
    </el-form-item>
    <el-form-item label="所属课程">
      <el-select style="width: 83%" v-model="searchForm.course_id" placeholder="请选择所属课程">
        <el-option
            v-for="item in option.course"
            :label="item.course_name"
            :value="item.course_id" />
      </el-select>
    </el-form-item>
    <el-form-item class="formFooter">
      <el-button @click="reset()">重置</el-button>
      <el-button @click="search()" type="primary">搜索</el-button>
    </el-form-item>
  </el-form>

</template>

<script setup>
import {onMounted, reactive, ref} from "vue";
import https from "@/apis/axio";
import {ElMessage} from "element-plus"

const emit = defineEmits(['search_paper'])

const option = reactive({
  course:[]
})
const searchForm = reactive({
  paper_name: '',
  paper_id:'',
  course_id:''
})

onMounted(()=>{
  https.post('/teacher/get_courses',{'username':JSON.parse(localStorage.getItem('token')).username}).then(res => {
    option.course = res.data
  })
})

function search() {
  https.post('/teacher/search_paper',searchForm).then(res => {
    res.data.forEach(item=>{
      item.catalog_name=item.catalog_name.join('，')
    })
    emit('search_paper',res.data)
  })
}

function reset() {
  searchForm.course_id=''
  searchForm.paper_name=''
  searchForm.paper_id=''
}

</script>

<style scoped lang="scss">
.search_title{
  display: block;
  font-size: 22px;
  font-weight: bold;
  padding-left: 10px;
  padding-top: 15px;
}
.searchForm{
  margin-top: 20px;
  margin-left: 10px;
}
.el-form-item{
  font-weight: bold;
  font-size: 5px;
}

.formFooter{
  float: right;
}

</style>
