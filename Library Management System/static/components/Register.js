export default {
    template: 
    `<div class="container" style="margin-top: 50px;">
        <div class="row mb-2">
            <div class="col-md-12 col-sm-12">
                <center><h2 class="mb-2 mt-2" style="color: #963E97;margin-top: 70px;">LIBRARY MANAGEMENT SYSTEM</h2></center>
            </div>
        </div>
        <div class="row justify-content-center align-items-center d-flex">
            <div class="col-md-3 col-sm-1"></div>
            <div class="col-md-6 col-sm-10">
                <div class="card" id="logincard">
                    <div class="card-body">
                        <center><h2 class="mb-2 mt-2" style="color: #963E97;">Register</h2></center>
                        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                            {{error}}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                        <!--<form action="/register" method="post">-->
                            <div class="row mb-2">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label for="loginuname">Username</label>
                                        <input type="text" name="username" id="loginuname" class="form-control form-control-sm" v-model="regcred.username" required>
                                    </div>
                                </div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label for="loginfname">Full Name</label>
                                        <input type="text" name="fullname" id="loginfname" class="form-control form-control-sm" v-model="regcred.fullname" pattern="[A-Za-z. ]*" title="Numeric values are not allowed." required>
                                    </div>
                                    <p class="text-danger" v-if="nameerror">{{ nameerror }}</p>
                                </div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label for="loginemail">Email</label>
                                        <input type="email" name="email" id="loginemail" class="form-control form-control-sm" v-model="regcred.email" required>
                                    </div>
                                </div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label for="loginpass">Password</label>
                                        <input type="password" name="password" id="loginpass" class="form-control form-control-sm" v-model="regcred.password" required> 
                                    </div>
                                    <p class="text-danger" v-if="pwderror">{{ pwderror }}</p>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label for="logincpass">Confirm Password</label>
                                        <input type="password" name="cpassword" id="logincpass" class="form-control form-control-sm" v-model="regcred.cpassword" required> 
                                    </div>
                                    <p class="text-danger" v-if="cpwderror">{{ cpwderror }}</p>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <center>
                                        <button type="submit" class="btn btn-primary btn-sm" @click='register'>Submit</button>&nbsp;&nbsp;&nbsp;
                                        <router-link class="btn btn-outline-primary btn-sm" to="/">Login</router-link>
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
            regcred: {
                "username": null,
                "fullname": null,
                "email": null,
                "password": null,
                "cpassword": null,
                "role": 'general_user',
            },
            error: null,
            nameerror: null,
            pwderror: null,
            cpwderror: null,
        }
    },

    methods: {
        async register(){
            this.error = null;
            this.pwderror = null;
            this.cpwderror = null;

            if (this.regcred.username==null || this.regcred.fullname==null || this.regcred.email==null || this.regcred.password==null || this.regcred.cpassword==null){
                this.error = "All fields are mandatory!";
                return;
            } else if (this.regcred.password.length < 6) {
                this.pwderror = "Password should be at least 6 characters!";
            } else if (this.regcred.password != this.regcred.cpassword){
                this.pwderror = "Password and Confirm password do not match!";
                this.cpwderror = "Password and Confirm password do not match!";
            } else {
                const res = await fetch('/userregister', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.regcred), //javascript object to json
                })
                const data = await res.json();    //json string to js object
                if(res.ok){
                    alert("Account created successfully! Proceed to Login.");
                    this.$router.push('/');
                }
                else {
                    this.error = data.message;
                }
            }
        }
    },
}