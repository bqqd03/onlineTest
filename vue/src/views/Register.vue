<template>
  <el-card header="账号注册" class="register_box">
    <el-form
        :model="registerForm"
        :rules="rules"
        label-width="80px"
        size="small">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="registerForm.username" placeholder="请输入用户名" autofocus />
      </el-form-item>
      <el-form-item label="真实姓名" prop="name">
        <el-input v-model="registerForm.name" placeholder="请输入真实姓名" autofocus />
      </el-form-item>
      <el-form-item label="性别" prop="sex">
        <el-radio-group v-model="registerForm.sex">
          <el-radio label="男">男</el-radio>
          <el-radio label="女">女</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="电子邮件" prop="email">
        <el-input v-model="registerForm.email" placeholder="请输入电子邮件"  />
      </el-form-item>
      <el-form-item label="电话号码" prop="phone">
        <el-input v-model="registerForm.phone" placeholder="请输入电话号码"  />
      </el-form-item>
      <el-form-item label="生日日期" prop="birthday">
        <el-date-picker
            v-model="registerForm.birthday"
            type="date"
            placeholder="请选择生日日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            :locale="locale"/>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input type="password" v-model="registerForm.password" placeholder="请输入密码" show-password />
      </el-form-item>
      <el-form-item label="确认密码" prop="check_password">
        <el-input type="password" v-model="registerForm.check_password" placeholder="请重新输入密码" show-password />
      </el-form-item>
      <el-form-item label="角色" prop="role">
        <el-select v-model="registerForm.role" placeholder="请选择角色" filterable allow-create default-first-option style="width: 100%">
          <el-option
              v-for="item in options"
              :label="item.label"
              :value="item.value"/>
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm()">注册</el-button>
        <el-button native-type="reset">重置</el-button>
        <el-button @click=" router.push('/login')" style="position: absolute;right: 0">返回</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import https from "@/apis/axio"
import { useRouter } from 'vue-router'
import { ElMessage } from "element-plus"
import zhCn from "element-plus/es/locale/lang/zh-cn"

let locale=zhCn
const router = useRouter()
const options = [
    {
        value: 'teacher',
        label: '教师',
    },
    {
        value: 'student',
        label: '学生',
    }
]

const registerForm = reactive({
  username: '',
  name: '',
  sex: '男',
  email: '',
  phone: '',
  birthday: '',
  password: '',
  check_password: '',
  role: '',
});

let validatePassword2 = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请再次输入密码'));
    } else if (value !== registerForm.password) {
        callback(new Error('两次输入密码不一致!'));
    } else {
        callback();
    }
};

const rules = {
  username: [
      { required: true, message: "用户名缺失", trigger: "blur" },
      { min: 3, max: 12, message: "长度在 3 到 12 个字符", trigger: "blur" },
  ],
  password: [
      { required: true, message: "请输入密码", trigger: "blur" },
      { min: 3, max: 15, message: "长度在 3 到 15 个字符", trigger: "blur" },
  ],
  check_password: [{ required: true, validator: validatePassword2, trigger: 'blur' }],
  role: [
    { required: true, message: "请选择角色", trigger: "blur" },
  ]
};


function submitForm(){
  https.post('/auth/register', registerForm).then(res=>{
      if (res.data.code===200){
          ElMessage({
              message: '注册成功',
              type: 'success',
          })
          router.push('/login')
      } else {
          ElMessage({
              message: res.data.message,
              type: 'error',
          })
      }
  }).catch(()=>{
    ElMessage.error('未连接到服务器')
  })
}

</script>


<style scss>
.register_box{
    width: 400px;
    padding: 0 20px;
    position: absolute;
    left: 50%;
    top:40%;
    transform: translate(-50%,-50%);
}

</style>