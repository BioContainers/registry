import { createApp } from 'vue'
import ViewUIPlus from 'view-ui-plus'
import 'view-ui-plus/dist/styles/viewuiplus.css'
import App from './App.vue'
import router from './router.js'

// GitHub Pages single-page fallback: restore the deep-link path saved by 404.html.
const redirect = sessionStorage.redirect
delete sessionStorage.redirect
if (redirect && redirect !== location.href) {
  const u = new URL(redirect)
  history.replaceState(null, '', u.pathname + u.search)
}

createApp(App).use(router).use(ViewUIPlus).mount('#app')
