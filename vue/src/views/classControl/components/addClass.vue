<template>
  <span class="add-title">添加班级</span>
  <el-form class="addForm">
    <el-form-item label="所属课程" label-width="80px">
      <el-select v-model="addForm.course_id" style="width: 150px;" placeholder="请选择所属课程">
        <el-option
            v-for="item in course.options"
            :key="item.course_id"
            :label="item.course_name"
            :value="item.course_id" />
      </el-select>
    </el-form-item>
    <el-form-item label="班级名称" label-width="80px">
      <el-input v-model="addForm.class_name" placeholder="请输入班级名称"/>
    </el-form-item>
    <el-form-item label="班级码" label-width="80px">
      <el-input v-model="addForm.class_code" placeholder="请输入班级码"/>
    </el-form-item>

    <el-form-item class="formFooter">
      <el-button @click="save()" type="primary">确 定</el-button>
    </el-form-item>
  </el-form>

</template>

<script setup>
import {onMounted, reactive, ref} from "vue";
import https from "@/apis/axio.js";
import {ElMessage} from "element-plus";

const myEmit = defineEmits(["getClassList"])
const course=reactive({
  options:[]
})
const addForm = reactive({
  class_name: '',
  class_code:'',
  course_id:''
})

onMounted(()=> {
  https.post('/teacher/get_courses',{'username':JSON.parse(localStorage.getItem('token')).username}).then(res => {
    course.options = res.data
  })
})

function save() {
  https.post('/teacher/add_class',addForm).then(res=>{
    if (res.data.code===200){
      ElMessage.success('添加成功')
      addForm.class_name=''
      // addForm.class_code=''
      // addForm.course_id=''
      myEmit('getClassList')
    } else {
      ElMessage.error(res.data.message)
    }
  })
}

</script>

<style scoped lang="scss">
.add-title{
  display: block;
  font-size: 22px;
  font-weight: bold;
  padding-left: 10px;
  padding-top: 15px;
}
.addForm{
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
