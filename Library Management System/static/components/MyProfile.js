export default {
    template:
    `<div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header">My Profile</div>
            <div class="card-body">
                <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{error}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <div class="form-group">
                            <label>Full Name</label>
                            <input type="text" class="form-control form-control-sm" v-model="userdetails.full_name" required>
                        </div>
                    </div>
                </div>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <div class="form-group">
                            <label>Username</label>
                            <input type="text" class="form-control form-control-sm" v-model="userdetails.username" readonly required>
                        </div>
                    </div>
                </div>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <div class="form-group">
                            <label>Email</label>
                            <input type="email" class="form-control form-control-sm" v-model="userdetails.email" required>
                        </div>
                    </div>
                </div>
                <br>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <button type="submit" class="btn btn-primary btn-sm" @click='editProfile'>Save Changes</button>&nbsp;&nbsp;&nbsp;
                        <!--<button type="submit" class="btn btn-danger btn-sm" @click='deleteAccount'>Delete Account</button>-->
                    </div>
                </div>
            </div>
        </div>
    </div>`,

    data(){
        return {
            userdetails: {
                "full_name": sessionStorage.getItem('full_name'),
                "username": sessionStorage.getItem('username'),
                "email": sessionStorage.getItem('email'),
            },
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
        }
    },

    methods: {

        async editProfile(){
            if (this.userdetails.full_name == null || this.userdetails.username == null || this.userdetails.email == null) {
                this.error = "All fields are mandatory!";
                return;
            } else {
                const res = await fetch('/editprofile', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.token,
                    },
                    body: JSON.stringify(this.userdetails),
                });
                if(res.ok){
                    const data = await res.json(); 
                    sessionStorage.setItem('username', data.newdetail.username);
                    sessionStorage.setItem('email', data.newdetail.email);
                    sessionStorage.setItem('full_name', data.newdetail.full_name);
                    alert(data.newdetail.message);
                    window.location.reload();
                } else {
                    const data = await res.json(); 
                    this.error = data.message;
                }
            }
        }
    },
}