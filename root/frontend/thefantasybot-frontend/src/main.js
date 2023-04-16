import { createApp } from 'vue';

// import './assets/main.css';
import App from './App.vue';
import ViewPlayers from './components/ViewPlayers.vue';

const app = createApp(App);

app.component('view-players', ViewPlayers);

app.mount('#app');
