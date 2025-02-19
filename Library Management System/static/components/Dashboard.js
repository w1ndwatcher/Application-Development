import UserDashboard from './UserDashboard.js'
import LibrarianDashboard from './LibrarianDashboard.js'

export default {
    template: `
    <div>
    <UserDashboard v-if="userRole=='general_user'"/>
    <LibrarianDashboard v-if="userRole=='librarian'"/>
    </div>`,
    data() {
        return {
            userRole: sessionStorage.getItem('role'),
            authToken: sessionStorage.getItem('auth-token'),
        }
    },
    components: {
        UserDashboard,
        LibrarianDashboard,
    }
}