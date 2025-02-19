export default {
    template:
    `<div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header">Users</div>
            <div class="card-body">
                <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{error}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                <table id="allsections" class="table table-striped" style="width:100%" v-if="users.length>0">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Last Active</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in users" :key="user.id">
                            <td>{{ user.full_name }}</td>
                            <td>{{ user.email }}</td>
                            <td>{{ user.last_activity }}</td>
                        </tr>
                    </tbody>
                </table>
                <div class="row mt-2 mb-2" v-else>
                    <div class="col-md-12 col-sm-12">
                        <p class="text-muted text-center"><i>No active users.</i></p>
                    </div>
                </div>
            </div>
        </div>
    </div>`,

    data(){
        return {
            users: [],
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
        }
    },

    async mounted(){
        await this.fetchUsers();
    },

    methods: {
        async fetchUsers(){
            const res = await fetch('/users', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            })
            if (res.status == 200) {
                const data = await res.json();
                this.users = data.users;
            } else {
                const data = await res.json(); 
                this.error = data.message;
            }
        },
    }
}