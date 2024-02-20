<template>
  <el-row :gutter="20">
    <el-col :span="7">
      <el-card>
        <template #header>
          <span>知识点</span>
          <el-button type="primary" @click="dialogAddVisible = true">添加章节</el-button>
        </template>

        <div style="margin-top: 15px">
          <el-scrollbar :style="{ height: scrollHeight }">
            <div class="fistBox" style="margin-bottom: 10px" v-for="catalog in catalogs.menuData" >
              <div style=" display: flex;">
                <ArrowDownBold  v-if="catalog.show" style="height: 15px;width: 15px;margin-top: 3px;margin-right: 5px " />
                <ArrowRightBold v-else style="height: 15px;width: 15px;margin-top: 3px;margin-right: 5px "/>
                <span style="cursor: pointer;font-size: 18px" @click="catalogShow(catalog.id)">{{catalog.label}}</span>
                <div style="position: absolute;right: 0">
                  <Plus fill="#333" size="20" style="margin-top: 2px;cursor: pointer" @click="dialogCatalogs('添加知识点',catalog)"/>
                  <EditTwo fill="#333" size="20" style="margin-top: 2px;margin-left: 3px;cursor: pointer "  @click="dialogCatalogs('修改知识点',catalog)"/>
                </div>
              </div>
              <div v-if="catalog.show" v-for="item in catalog.children"  style="display: flex;margin-left: 20px">
                <span style="margin-left: 23px;margin-top: 8px;cursor: pointer;font-size: 16px" @click="getContext(item)">{{item.label}}</span>
                <div style="position: absolute;right: 0">
                  <el-popconfirm
                      title="确定要删除吗？"
                      confirm-button-text="确定"
                      cancel-button-text="取消"
                      @confirm="deleteCatalog(item)"
                      v-if="item.isEdit === 0">
                    <template #reference>
                      <DeleteFour  fill="#333" size="20" style="margin-top: 10px;cursor: pointer"  />
                    </template>
                  </el-popconfirm>
                  <EditTwo fill="#333" size="20" style="margin-top: 10px;margin-left: 3px;cursor: pointer "  @click="dialogCatalogs('修改知识点',catalog)"/>
                </div>
              </div>
            </div>
          </el-scrollbar>
        </div>
      </el-card>
    </el-col>

    <el-col :span="17">
      <el-card>
        <template #header>
          <div>
            <text style="margin-right: 15px">课程名:</text>
            <el-select  style="width: 240px" v-model="course.value" placeholder="课程切换">
              <el-option
                  v-for="item in course.courseOption"
                  :key="item.course_id"
                  :label="item.course_name"
                  :value="item.course_id">
              </el-option>
            </el-select>
        </div>
        <div>
          <el-button type="primary" @click.prevent="addQuestion()" :icon="DocumentAdd">添加题目</el-button>
          <el-button :icon="FolderOpened">导入题目</el-button>
        </div>
        </template>
        <div>
          <span>题型</span>
          <el-radio-group v-model="search.searchStyle" class="search-radio" @change="searchQuestion"  >
            <el-radio-button label="全部" />
            <el-radio-button label="单选">单选题</el-radio-button>
            <el-radio-button label="多选">多选题</el-radio-button>
            <el-radio-button label="填空">填空题</el-radio-button>
            <el-radio-button label="判断">判断题</el-radio-button>
            <el-radio-button label="问答">问答题</el-radio-button>
          </el-radio-group>
        </div>

        <div>
          <span>难度</span>
          <el-radio-group v-model="search.searchDegree" class="search-radio" @change="searchQuestion">
            <el-radio-button label="全部" />
            <el-radio-button label="简单" />
            <el-radio-button label="普通" />
            <el-radio-button label="困难" />
          </el-radio-group>
        </div>



        <div class="space">
          <span style="padding: 6px 0">题目</span>
        </div>
        <el-scrollbar :style="{ height: scrollCardHeight }">
          <single-show :singles="options.singles" @getQuestion="getQuestion" @getMenuList="getMenuList" />
          <multiple-show :multiples="options.multiples" @getQuestion="getQuestion" @getMenuList="getMenuList" />
          <judgment-show :judgments="options.judgments" @getQuestion="getQuestion" @getMenuList="getMenuList" />
          <blank-show :blanks="options.blanks" @getQuestion="getQuestion" @getMenuList="getMenuList" />
          <answer-show :answers="options.answers" @getQuestion="getQuestion" @getMenuList="getMenuList" />
        </el-scrollbar>
      </el-card>
    </el-col>
  </el-row>


  <el-dialog v-model="dialogFormVisible" :title="catalogFormDialog.title" draggable width="35%">
    <el-divider style="margin-top: -20px" />
    <el-form :model="catalogFormDialog" style="margin-top: -10px" label-width="95px" label-position="left">
      <el-form-item label="章节名称" >
        <span>{{catalogFormDialog.contextLabel}}</span>
      </el-form-item>
      <el-form-item label="知识点代码" >
        <el-input v-if="catalogFormDialog.title==='添加知识点'" v-model="catalogFormDialog.id" placeholder="请输入知识点代码" style="width: 60%"></el-input>
        <span v-else>{{ catalogFormDialog.id }}</span>
      </el-form-item>
      <el-form-item label="知识点名称" >
        <el-input v-model="catalogFormDialog.label" placeholder="请输入知识点名称" style="width: 60%"></el-input>
      </el-form-item>
      <div style="position: absolute;right: 0;margin-top: -15px;margin-right: 20px">
        <el-button @click="saveCatalog()" type="primary">确 定</el-button>
        <el-button @click="dialogFormVisible = false">取 消</el-button>
      </div>
    </el-form>
  </el-dialog>

  <el-dialog v-model="dialogAddVisible" title="添加章节" draggable width="35%">
    <el-divider style="margin-top: -20px" />
    <el-form :model="catalogAddDialog" style="margin-top: -10px" label-width="95px" label-position="left">
      <el-form-item label="章节代码" >
        <el-input v-model="catalogAddDialog.id" placeholder="请输入章节代码" style="width: 60%"></el-input>
      </el-form-item>
      <el-form-item label="章节名称" >
        <el-input v-model="catalogAddDialog.label" placeholder="请输入章节名称" style="width: 60%"></el-input>
      </el-form-item>
      <div style="position: absolute;right: 0;margin-top: -15px;margin-right: 20px">
        <el-button @click="addCatalogs()" type="primary">确 定</el-button>
        <el-button @click="dialogAddVisible = false">取 消</el-button>
      </div>
    </el-form>
  </el-dialog>


</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import SingleShow from "./components/singleShow.vue"
import MultipleShow from "./components/multipleShow.vue"
import JudgmentShow from "./components/judgmentShow.vue"
import BlankShow from "./components/blankShow.vue"
import AnswerShow from "./components/answerShow.vue"
import { Plus, EditTwo, DeleteFour } from '@icon-park/vue-next'
import https from "@/apis/axio"
import { DocumentAdd, FolderOpened } from '@element-plus/icons-vue'
import { useRouter } from "vue-router";
import {ElMessage} from "element-plus";

const scrollHeight = (document.documentElement.clientHeight - 200).toString() + "px"
const scrollCardHeight = (document.documentElement.clientHeight - 340).toString() + "px"
const dialogFormVisible=ref(false)
const dialogAddVisible=ref(false)
const catalogs=reactive({
  menuData:[],
  value:''
})

const router = useRouter()
const course = reactive({
  courseOption:[],
  vale:''
})
const search = reactive({
  searchStyle:'全部',
  searchDegree:'全部',
  searchID:''
})
const options=reactive({
  singles:[],
  multiples:[],
  judgments:[],
  blanks:[],
  answers:[]
})

let token = {
  Authorization: localStorage.getItem('token')
}
const catalogFormDialog=reactive({
  id:'',
  pid:'',
  contextLabel:'',
  label:'',
  course_id:'',
  isEdit:'0',
  title:''
})
const catalogAddDialog=reactive({
  id:'',
  label:'',
  course_id:'',
  isEdit:'0',
})

onMounted(()=> {
  https.post('/teacher/get_courses',{'username':JSON.parse(localStorage.getItem('token')).username}).then(res => {
    course.courseOption = res.data
    course.value = course.courseOption[0].course_id
  })
})

watch(() => course.value, (newCourse) => {
  getMenuList(newCourse)
  getQuestion(newCourse)
})




// 获取题目
function getQuestion (e, type='课程') {
  https.post('/teacher/get_singles', {'identify_id':e,'identify_type':type}).then(res=>{
    options.singles=res.data
  })
  https.post('/teacher/get_multiples', {'identify_id':e,'identify_type':type}).then(res=>{
    options.multiples=res.data
  })
  https.post('/teacher/get_judgements', {'identify_id':e,'identify_type':type}).then(res=>{
    options.judgments=res.data
  })
  https.post('/teacher/get_blanks', {'identify_id':e,'identify_type':type}).then(res=>{
    options.blanks=res.data
  })
  https.post('/teacher/get_answers', {'identify_id':e,'identify_type':type}).then(res=>{
    options.answers=res.data
  })
}

// 获取知识点
function getMenuList (e) {
  https.post("/teacher/get_catalog",{'course':e}).then(res => {
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
      getQuestion(course.value)
    } else {
      item.show = false
    }
  })
  search.searchStyle='全部'
  search.searchDegree='全部'
  search.searchID=''
  catalogs.value= ''
}
function addQuestion() {
  router.push( "/add_question")
}

function getContext(e) {
  search.searchStyle='全部'
  search.searchDegree='全部'
  search.searchID=''
  catalogs.value= e.id

  getQuestion(e.id,'知识点')
}

function searchQuestion() {
  let identify_type
  let identify_id
  if (catalogs.value===''){
    identify_type='课程'
    identify_id = course.value
  } else {
    identify_type='知识点'
    identify_id = catalogs.value
  }
  https.post('/teacher/search_questions', {'identify_id':identify_id,'identify_type':identify_type,'searchStyle':search.searchStyle,'searchDegree':search.searchDegree}).then(res=>{
    options.singles=res.data.singles
    options.multiples=res.data.multiples
    options.judgments=res.data.judgments
    options.blanks=res.data.blanks
    options.answers=res.data.answers
  })
}

function addCatalogs() {
  catalogAddDialog.course_id = course.value
  https.post('/teacher/add_catalog', catalogAddDialog).then(res => {
    if (res.data.code === 200) {
      ElMessage.success('添加成功')
      dialogAddVisible.value = false
      catalogAddDialog.label=''
      catalogAddDialog.id = ''
      getMenuList(course.value)
      getQuestion(course.value)
    } else {
      ElMessage.error(res.data.message)
    }
  })
}

function dialogCatalogs(title, data){
  window.localStorage.setItem('catalog', JSON.stringify(data))
  catalogFormDialog.label=''
  catalogFormDialog.id = ''
  dialogFormVisible.value = true
  catalogFormDialog.title = title
  catalogFormDialog.course_id = course.value

  if (data.pid===null){
    catalogFormDialog.contextLabel = JSON.parse(window.localStorage.getItem('catalog')).label
  } else {
    catalogs.menuData.forEach(function (datas) {
      if (data.pid === datas.id){
        catalogFormDialog.contextLabel = datas.label
      }
    })
  }

  if (title === '修改知识点'){
    catalogFormDialog.id = JSON.parse(window.localStorage.getItem('catalog')).id
    catalogFormDialog.label = JSON.parse(window.localStorage.getItem('catalog')).label
    catalogFormDialog.pid = JSON.parse(window.localStorage.getItem('catalog')).pid
  }
}

function saveCatalog() {
  if (catalogFormDialog.title==='添加知识点'){
    catalogFormDialog.pid = JSON.parse(window.localStorage.getItem('catalog')).id
    https.post('/teacher/add_catalog', catalogFormDialog).then(res=>{
      if (res.data.code === 200){
        ElMessage.success('添加成功')
        dialogFormVisible.value = false
        getMenuList(course.value)
        getQuestion(course.value)
      } else {
        ElMessage.error(res.data.message)
      }
    })
  } else {
    https.post('/teacher/edit_catalog', catalogFormDialog).then(res=>{
      if (res.data.code === 200){
        ElMessage.success('修改成功')
        dialogFormVisible.value = false
        getMenuList(course.value)
        getQuestion(course.value)
      } else {
        ElMessage.error(res.data.message)
      }
    })
  }
}
function deleteCatalog(e) {
  https.post('/teacher/delete_catalog', {'catalog_id':e.id}).then(res=>{
    if (res.data.code === 200){
      ElMessage.success('删除成功')
      getMenuList(course.value)
      getQuestion(course.value)
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
.search-radio {
  margin: 0 0 10px 10px;
}
.space {
  display: flex;
  justify-content: space-between;
  padding: 2px 20px ;
  border: 1px solid #d3d3d3;
  background: #f5f5f5;
  margin-bottom: 13px;
}
.fistBox :hover{
  background-color: #F5F5F5;
}
</style>
