<template>
  <el-popover  placement="bottom" trigger="hover" width="500px">
    <el-divider style="margin: 10px 0" />
    <span style="font-size: 5px;margin-left: 10px">极限 Limits</span>
    <el-divider  style="margin: 10px 0 -10px" />
    <el-button @click="emit('question','\\lim  ')" class="btn">
      <el-image src="/assets/Latex/array01/limit01.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\lim_{x \\to 0} ')" class="btn">
      <el-image src="/assets/Latex/array01/limit02.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\lim_{x \\to \\infty}  ')" class="btn">
      <el-image src="/assets/Latex/array01/limit03.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\textstyle \\lim_{x \\to 0}  ')" class="btn" >
      <el-image src="/assets/Latex/array01/limit04.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\max_{}  ')" class="btn">
      <el-image src="/assets/Latex/array01/limit05.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\min_{}  ')" class="btn">
      <el-image src="/assets/Latex/array01/limit06.png" style="height: 45px" />
    </el-button>

    <el-divider style="margin: 10px 0" />
    <span style="font-size: 5px;margin-left: 10px">对数指数 Logarithms and exponentials</span>
    <el-divider  style="margin: 10px 0" />
    <el-button @click="emit('question','\\log_{}{}  ')" class="btn">
      <el-image src="/assets/Latex/array01/log01.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\lg_{}{} ')" class="btn">
      <el-image src="/assets/Latex/array01/log02.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\ln_{}{}  ')" class="btn">
      <el-image src="/assets/Latex/array01/log03.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\exp  ')" class="btn" >
      <el-image src="/assets/Latex/array01/limit04.png" style="height: 45px" />
    </el-button>

    <el-divider style="margin: 10px 0" />
    <span style="font-size: 5px;margin-left: 10px">界限 Bounds</span>
    <el-divider  style="margin: 10px 0" />
    <el-button @click="emit('question','\\min x  ')" class="btn">
      <el-image src="/assets/Latex/array01/bound01.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\max x ')" class="btn">
      <el-image src="/assets/Latex/array01/bound02.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\sup t  ')" class="btn">
      <el-image src="/assets/Latex/array01/bound03.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\inf s  ')" class="btn" >
      <el-image src="/assets/Latex/array01/bound04.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\lim u  ')" class="btn">
      <el-image src="/assets/Latex/array01/bound05.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\limsup w ')" class="btn">
      <el-image src="/assets/Latex/array01/bound06.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\liminf v  ')" class="btn">
      <el-image src="/assets/Latex/array01/bound07.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\dim p  ')" class="btn" >
      <el-image src="/assets/Latex/array01/bound08.png" style="height: 45px" />
    </el-button>
    <el-button @click="emit('question','\\ker\\phi  ')" class="btn" >
      <el-image src="/assets/Latex/array01/bound09.png" style="height: 45px" />
    </el-button>


    <template #reference>
      <el-button style="padding: 0">
        <img src="/assets/Latex/array01/limits.png" style="width: 80px">
      </el-button>
    </template>
  </el-popover>

</template>

<script setup>
import { defineEmits } from 'vue'


const emit=defineEmits(['question'])
</script>

<style>
.btn{
  padding: 0;
  margin: 20px 0 -20px 5px;
  background-color: #f8f9fa;
  border-color: #ffffff;
}

</style>