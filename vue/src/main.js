import { createApp } from 'vue'
import App from './App.vue'

import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import "@icon-park/vue-next/styles/index.css"
import Router from './router/index.js'
import VueLatex from 'vatex'
import VueCropper from 'vue-cropper';
import 'vue-cropper/dist/index.css'

const app = createApp(App)


app.use(ElementPlus)
app.use(Router)
app.use(VueLatex)
app.use(VueCropper)

app.mount('#app')
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}