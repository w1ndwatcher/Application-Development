export default {
    template: 
    `<div class="d-flex flex-column flex-shrink-0 p-3 bg-light col-md-2 col-sm-2" style="height: 100vh;position: fixed;z-index: 1020;">
        <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none">
            <span class="fs-4">{{ username }}</span>
        </a>
        <hr>
        <ul class="nav nav-pills flex-column mb-auto" v-if="role==='librarian'">
            <li>
                <router-link class="nav-link link-dark mb-2 col-md-12 col-sm-8" :class="{ 'active': $route.path === '/dashboard' }" to="/dashboard">
                    <i class="fa fa-chart-line me-2" width="16" height="16"></i>
                    <span class="d-sm-none d-md-inline">DASHBOARD</span>
                </router-link>
            </li>
            <li>
                <router-link class="nav-link link-dark mb-2 col-md-12 col-sm-8" :class="{ 'active': $route.path === '/allrequests' }" to="/allrequests">
                    <i class="fa fa-stamp me-2" width="16" height="16"></i>
                    <span class="d-sm-none d-md-inline">REQUESTS</span>
                </router-link>
            </li>
            <li>
                <router-link class="nav-link link-dark mb-2 col-md-12 col-sm-8" :class="{ 'active': $route.path === '/section' }" to="/section">
                    <i class="fa fa-database me-2" width="16" height="16"></i>
                    <span class="d-sm-none d-md-inline">SECTIONS</span>
                </router-link>
            </li>
            <li>
                <router-link class="nav-link link-dark mb-2 col-md-12 col-sm-8" :class="{ 'active': $route.path === '/allbooks' }" to="/allbooks">
                    <i class="fa fa-book me-2" width="16" height="16"></i>
                    <span class="d-sm-none d-md-inline">BOOKS</span>
                </router-link>
            </li>
            <li>
                <router-link class="nav-link link-dark mb-2 col-md-12 col-sm-8" :class="{ 'active': $route.path === '/issuehistory' }" to="/issuehistory">
                    <i class="fa fa-clock me-2" width="16" height="16"></i>
                    <span class="d-sm-none d-md-inline">HISTORY</span>
                </router-link>
            </li>
            <li>
                <router-link class="nav-link link-dark col-md-12 col-sm-8" :class="{ 'active': $route.path === '/userprofiles' }" to="/userprofiles">
                    <i class="fa fa-user me-2" width="16" height="16"></i>
                    <span class="d-sm-none d-md-inline">USER PROFILES</span>
                </router-link>
            </li>
        </ul>
        <ul class="nav nav-pills flex-column mb-auto" v-else>
            <li>
                <router-link class="nav-link link-dark mb-2 col-md-12 col-sm-8" :class="{ 'active': $route.path === '/dashboard' }" to="/dashboard">
                    <i class="fa fa-chart-line me-2" width="16" height="16"></i>
                    <span class="d-sm-none d-md-inline">DASHBOARD</span>
                </router-link>
            </li>
            <li>
                <router-link class="nav-link link-dark mb-2 col-md-12 col-sm-8" :class="{ 'active': $route.path === '/allbooks' }" to="/allbooks">
                    <i class="fa fa-book me-2" width="16" height="16"></i>
                    <span class="d-sm-none d-md-inline">BOOKS</span>
                </router-link>
            </li>
            <li>
                <router-link class="nav-link link-dark mb-2 col-md-12 col-sm-8" :class="{ 'active': $route.path === '/usersections' }" to="/usersections">
                    <i class="fa fa-database me-2" width="16" height="16"></i>
                    <span class="d-sm-none d-md-inline">SECTIONS</span>
                </router-link>
            </li>
            <li>
                <router-link class="nav-link link-dark mb-2 col-md-12 col-sm-8" :class="{ 'active': $route.path === '/mybooks' }" to="/mybooks">
                    <i class="fa fa-bookmark me-2" width="16" height="16"></i>
                    <span class="d-sm-none d-md-inline">MY BOOKS</span>
                </router-link>
            </li>
        </ul>
    </div>`,

    data(){
        return {
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
            username: sessionStorage.getItem('username'),
        }
    },
}