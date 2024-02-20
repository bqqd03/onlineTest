<template>
  <el-card v-for="(item) in props.singles" :key="item.id" style="margin-bottom: 12px">
    <div class="card-header">
      <div>
        <span style="color: #409eff;">【单选题】</span>
        <span class="degree">难度：{{ item.degree }}</span>
      </div>
      <div>
        <EditTwo fill="#333" size="20" style="margin-top: 10px;margin-right: 5px;cursor: pointer "  @click="editQuestion(item)"/>
        <el-popconfirm
            title="确定要删除吗？"
            confirm-button-text="确定"
            cancel-button-text="取消"
            @confirm="deleteQuestion(item)">
          <template #reference>
            <DeleteFour  fill="#333" size="20" style="margin-top: 10px;cursor: pointer"  />
          </template>
        </el-popconfirm>
      </div>
    </div>

    <div class="general-margin">
      <div class="general-flex" >
        <i/><text>{{ item.question }}</text>
      </div>
    </div>

    <div style="margin-left: 10px;display: flex;flex-flow: column;" >
      <el-radio label="A" :model-value=item.answer>A、{{ item.optionsA }}</el-radio>
      <el-radio label="B" :model-value=item.answer>B、{{ item.optionsB }}</el-radio>
      <el-radio label="C" :model-value=item.answer>C、{{ item.optionsC }}</el-radio>
      <el-radio label="D" :model-value=item.answer>D、{{ item.optionsD }}</el-radio>
    </div>

    <el-divider border-style="dashed" class="general-margin"/>

    <div style="display: flex;align-items: center;">
      <span style="font-weight: bold;color: #888;font-size: small;margin-right: 5px">参考答案</span>
      <strong>{{ item.answer }}</strong>
    </div>

    <el-divider border-style="dashed" class="general-margin"></el-divider>
    <div style="display: flex;">
      <span style="font-weight: bold;color: #888;font-size: small;margin-right: 5px">知识点</span>
      <span class="content">{{ item.knowledge_label }}</span>
    </div>
  </el-card>

</template>

<script setup>
import https from '@/apis/axio.js'
import { ElMessage } from "element-plus"
import { useRouter } from "vue-router"
import { DeleteFour, EditTwo } from "@icon-park/vue-next";
import { VueLatex } from "vatex";

const emits = defineEmits(["getQuestion","getMenuList"])
const router = useRouter()
const props = defineProps({
  singles:Object
})

function deleteQuestion(e) {
  https.post('/teacher/delete_question', {'question_id':e.id,'question_type':'单选题'}).then(res=>{
    if (res.data.code === 200){
      ElMessage.success('删除成功')
      emits("getQuestion",e.course_id)
      emits("getMenuList",e.course_id)
    } else {
      ElMessage.error(res.data.message)
    }
  })
}
function editQuestion(e) {
  e.type = '单选题'
  window.localStorage.setItem('question_data', JSON.stringify(e))
  router.push("/edit_question")
}

</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.general-icon {
  margin-right: 8px;
  width: 20px;
  height: 20px;
}
.general-flex{
  display: flex;
  align-items: center;
  i{
    width: 4px;
    height: 4px;
    border-radius: 50%;
    border: 2px solid #409eff;
    margin-right: 5px;
  }
}
.general-margin{
  margin: 12px 0;
}
.select {
  display: flex;
}
.degree{
  background: #f2f2f2;
  padding: 3px 10px;
  text-align: center;
  border-radius: 3px;
  font-size: small;
  margin-left: 10px;
}
.content{
  font-size: small;
  border: 1px #ddd solid;
  padding: 3px 10px;
  margin-left: 5px;
  margin-top: -3px;
  border-radius: 3px;
  text-align: center;
}
</style>