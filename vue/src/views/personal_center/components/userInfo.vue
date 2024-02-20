<template>
  <el-form class="infoForm" label-position="left">
    <el-form-item label="用户名" label-width="70px">
      <el-input v-model="editForm.username" placeholder="请重新输入用户名" />
    </el-form-item>
    <el-form-item label="真实姓名" label-width="70px">
      <el-input v-model="editForm.name" placeholder="请重新输入用户名" />
    </el-form-item>

    <el-form-item label="性别" label-width="70px">
      <el-radio-group v-model="editForm.sex">
        <el-radio label="男">男</el-radio>
        <el-radio label="女">女</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="邮箱" label-width="70px">
      <el-input v-model="editForm.email" placeholder="请重新输入邮箱" />
    </el-form-item>
    <el-form-item label="电话号码" prop="phone">
      <el-input v-model="editForm.phone" placeholder="请输入电话号码"  />
    </el-form-item>
    <el-form-item label="生日日期" prop="birthday">
      <el-date-picker
          v-model="editForm.birthday"
          type="date"
          placeholder="请选择生日日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"/>
    </el-form-item>
    <el-form-item label="所教课程" label-width="70px" v-if="role==='teacher'">
        <text>{{ editForm.class_type }}</text>
    </el-form-item>

    <el-form-item label="所属班级" label-width="70px" v-if="role==='student'">
      <text>{{ editForm.class_type }}</text>
    </el-form-item>

    <el-form-item class="formFooter">
      <el-button @click="saveInfo()" type="primary">确 定</el-button>
    </el-form-item>
  </el-form>

</template>

<script setup>
import {onMounted, reactive, ref} from "vue"
import https from "@/apis/axio"
import {ElMessage} from "element-plus"

let role = JSON.parse(localStorage.getItem('token')).role
let editForm=reactive({
  user_id:JSON.parse(localStorage.getItem('token')).user_id,
  username:'',
  name:'',
  birthday:'',
  email:'',
  phone:'',
  sex:'',
  class_type:''
})
onMounted(()=>{
  getUserInfo()

})

function getUserInfo() {
  https.post('/auth/get_userInfo',{'user_id':JSON.parse(localStorage.getItem('token')).user_id}).then(res=>{
    editForm.username = res.data.username
    editForm.name = res.data.name
    editForm.birthday = res.data.birthday
    editForm.email = res.data.email
    editForm.phone = res.data.phone
    editForm.sex = res.data.sex
    editForm.class_type = res.data.class_type
  })
}

function saveInfo() {
  https.post('/auth/user_edit',editForm).then(res=>{
      if (res.data.code===200){
        ElMessage.success('修改成功')
        window.localStorage.setItem('token',JSON.stringify(res.data.user))
        getUserInfo()
      } else {
        ElMessage.error(res.data.message)
      }
  }).catch(()=>{
    ElMessage.error('未连接到服务器')
  })
}

</script>

<style lang="scss" scoped>
.infoForm{
    width: 30%;
}

</style>
