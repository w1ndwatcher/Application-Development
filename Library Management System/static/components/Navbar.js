export default {
    template: 
    `<nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top" style="z-index: 1030;">
        <div class="container-fluid">
            <a class="navbar-brand text-white" href="/">LMS</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        Library Management System
                    </li>
                </ul>
                <ul class="navbar-nav mb-2 mb-lg-0 d-flex">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Settings
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                            <li><router-link class="dropdown-item" to="/myprofile">My Profile</router-link></li>
                            <li><a class="dropdown-item" @click='logout'>Logout</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>`,

    data() {
        return{
            role: sessionStorage.getItem('role'),
            token: sessionStorage.getItem('auth_token'),
        }
    },

    methods: {
        logout() {
            sessionStorage.removeItem('auth_token');
            sessionStorage.removeItem('role');
            sessionStorage.clear();
            this.$router.push('/');
        },
    },
    
}