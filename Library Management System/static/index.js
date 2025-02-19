import router from './router.js'
import Navbar from './components/Navbar.js';
import Sidebar from './components/Sidebar.js';

new Vue({
    el: "#app",
    template: `
    <div v-if="showElement">
        <Navbar />
        <div class="container-fluid">
            <div class="row">
                <Sidebar />
                <main class="col-md-9 ms-sm-auto col-lg-10 col-sm-10 px-4">
                    <router-view></router-view>
                </main>
            </div>
        </div>
    </div>
    <div v-else>
        <router-view></router-view>
    </div>`,
    router,
    components: {Navbar, Sidebar},
    computed: {
        showElement() {
          return !['/', '/register', '/forgotpass', '/enterotp', '/resetpassword'].includes(this.$route.path);
        }
    },
})