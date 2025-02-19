//import { createRouter, createWebHistory } from 'vue-router';
import Login from './components/Login.js'
import Register from './components/Register.js'
import ForgotPassword from './components/ForgotPassword.js';
import EnterOtp from './components/EnterOtp.js';
import ResetPassword from './components/ResetPassword.js';
import Dashboard from './components/Dashboard.js';
import Section  from './components/Section.js';
import AllBooks from './components/AllBooks.js';
import AddEbook from './components/AddEbook.js';
import ViewEbooks from './components/ViewEbooks.js';
import UserSections from './components/UserSections.js';
import UserEbooks from './components/UserEbooks.js';
import ReadEbook from './components/ReadEbook.js';
import EditSection from './components/EditSection.js';
import AllRequests from './components/AllRequests.js';
import EditEbook from './components/EditEbook.js';
import MyProfile from './components/MyProfile.js';
import UserProfiles from './components/UserProfiles.js';
import IssueHistory from './components/IssueHistory.js';

const routes = [
    { path: '/', component: Login },
    { path: '/register', component: Register },
    { path: '/forgotpass', component: ForgotPassword },
    { path: '/enterotp', component: EnterOtp },
    { path: '/resetpassword', component: ResetPassword },
    { path: '/dashboard', component: Dashboard },
    { path: '/section', component: Section },
    { path: '/editsection', component: EditSection },
    { path: '/allbooks', component: AllBooks },
    { path: '/addebook', component: AddEbook },
    { path: '/editebook', component: EditEbook },
    { path: '/viewebooks', component: ViewEbooks },
    { path: '/usersections', component: UserSections },
    { path: '/mybooks', component: UserEbooks },
    { path: '/read_ebook', component: ReadEbook },
    { path: '/allrequests', component: AllRequests },
    { path: '/myprofile', component: MyProfile },
    { path: '/userprofiles', component: UserProfiles },
    { path: '/issuehistory', component: IssueHistory }
];


export default new VueRouter({
    routes,
})



// const router = new VueRouter({
//     routes,
// });

// router.beforeEach((to, from, next) => {
//     const isAuthenticated = false; 
//     if (to.name !== 'Login' && !isAuthenticated) next({ name: 'Login' });
//     else next();
// });

// export default router;


// const router = createRouter({
//     history: createWebHistory(),
//     routes,
// });

//export default router;