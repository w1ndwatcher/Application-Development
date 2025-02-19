export default {
    template: 
    `<div class="container" style="margin-top: 70px;">
        <div class="row mb-2">
            <div class="col-md-12 col-sm-12">
                <center><h2 class="mb-2 mt-2" style="color: #963E97;margin-top: 100px;">LIBRARY MANAGEMENT SYSTEM</h2></center>
            </div>
        </div>
        <div class="row justify-content-center align-items-center d-flex">
            <div class="col-md-3 col-sm-1"></div>
            <div class="col-md-6 col-sm-10">
                <div class="card" id="logincard">
                    <div class="card-body">
                        <center><h2 class="mb-2 mt-2" style="color: #963E97;">Login</h2></center>
                        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                            {{error}}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                        <!--<form action="/login" method="post">-->
                            <div class="row mb-2">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label for="loginemail">Email</label>
                                        <input type="email" name="email" id="loginemail" class="form-control form-control-sm" v-model="logincred.email" required>
                                    </div>
                                </div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label for="loginpass">Password</label>
                                        <input type="password" name="password" id="loginpass" class="form-control form-control-sm" v-model="logincred.password" required> 
                                    </div>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-sm-12">
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" name="role" value="librarian" id="loginrole" @change="updaterole">
                                        <label class="form-check-label" for="loginrole">
                                            I am the Librarian
                                        </label>
                                    </div>
                                </div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-sm-12 text-end">
                                    <router-link to="/forgotpass">Forgot Password?</router-link>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <center>
                                        <a class="btn btn-outline-primary btn-sm" href="/#/register">Register</a>&nbsp;&nbsp;&nbsp;
                                        <button type="submit" class="btn btn-primary btn-sm" @click='loginsub'>Submit</button>
                                    </center>
                                </div>
                            </div>
                        <!--</form>-->
                    </div>
                </div>
            </div>
            <div class="col-md-3 col-sm-1"></div>
        </div>
    </div>`,
    data(){
        return {
            logincred: {
                "email": null,
                "password": null,
                "role": 'general_user',
            },
            error: null,
        }
    },
    methods: {
        updaterole(event){
            this.logincred.role = event.target.checked ? 'librarian' : 'general_user';
        },
        
        async loginsub(){
            console.log(this.logincred.role);
            const res = await fetch('/userlogin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.logincred), //javascript object to json
            })
            const data = await res.json();    //json string to js object
            if(res.ok){
                console.log(data);
                sessionStorage.setItem('auth-token', data.token);
                sessionStorage.setItem('role', data.role);
                sessionStorage.setItem('username', data.username);
                sessionStorage.setItem('email', data.email);
                sessionStorage.setItem('full_name', data.full_name);
                this.$router.push('/dashboard');
            }
            else {
                this.error = data.message;
            }
        },
    },
}