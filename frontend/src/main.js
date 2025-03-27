import { createApp } from 'vue'  // Mudar de 'vue' para 'vue'
import App from './App.vue'
import axios from 'axios'

const app = createApp(App)

axios.defaults.baseURL = 'http://localhost:5000/api'
app.config.globalProperties.$http = axios  // Disponibiliza globalmente

app.mount('#app')