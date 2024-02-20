<template>
  <el-row :gutter="75">
    <el-col :span="17" >
      <el-card>
        <template #header>
          <span>班级学生</span>
          <el-button @click="router.push('class_control')" type="primary">返回</el-button>
        </template>
        <el-scrollbar :style="{ height: scrollHeight }">
          <el-table :data="classStu" style="width: 100%;height: 100%" >
            <el-table-column type="index"  label="#" width="35" />
            <el-table-column align="center" label="头像" width="70">
              <template #default="scope">
                <el-avatar :src="scope.row.avatar"/>
              </template>
            </el-table-column>
<!--            <el-table-column prop="user_id" label="学生ID" width="80" align="center"  />-->
            <el-table-column prop="name" label="学生姓名" width="100" />
            <el-table-column prop="sex" label="性别" width="70" />
            <el-table-column prop="class_type" label="所属班级" width="100">
              <template #default="scope">
                <el-space>{{ className }}</el-space>
              </template>
            </el-table-column>
            <el-table-column prop="email" label="电子邮件" width="180" />
            <el-table-column prop="phone" label="手机号码" width="150" />
            <el-table-column prop="birthday" label="出生日期" width="150" />

            <el-table-column align="center" label="操作" width="150">
              <template #default="scope">
                <el-button type="danger" @click="getOut(scope.row)">踢出</el-button>
              </template>
            </el-table-column>

          </el-table>
        </el-scrollbar>
      </el-card>
    </el-col>

    <el-col :span="7" >
      <el-card>
        <class-applicat  @getClassStu="getClassStu" :class_id="route.query.class_id"></class-applicat>
      </el-card>
    </el-col>
  </el-row>

</template>

<script setup>
import {onMounted, ref} from "vue";
import https from "@/apis/axio.js";
import {ElMessage} from "element-plus";
import {useRoute,useRouter} from "vue-router";
import ClassApplicat from "../components/classApplicat.vue";

let classStu=ref()
let className=ref()
const route = useRoute()
const scrollHeight = (document.documentElement.clientHeight - 200).toString() + "px"
const router=useRouter()


onMounted(()=>{
  getClassStu()
})

function getClassStu() {
  https.post('/teacher/class_student',{'class_id':route.query.class_id}).then(res=>{
    classStu.value=res.data.data
    className.value=res.data.class_name
  }).catch(()=>{
    ElMessage.error('未连接到服务器')
  })
}

function getOut(item) {
  https.post('/teacher/delete_student',{'class_id':route.query.class_id,'stu_id':item.user_id}).then(res=>{
    if (res.data.code===200){
      ElMessage.success('删除成功')
      getClassStu()
    }
  }).catch(()=>{
    ElMessage.error('未连接到服务器')
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
.add-title{
  display: block;
  font-size: 22px;
  font-weight: bold;
  padding-left: 10px;
  padding-top: 15px;
}
</style>
