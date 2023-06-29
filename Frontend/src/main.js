import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import VueClipBoard from 'vue-clipboard3'

const app = createApp(App)
app.use(ElementPlus)
app.use(VueClipBoard)
app.mount('#app')
