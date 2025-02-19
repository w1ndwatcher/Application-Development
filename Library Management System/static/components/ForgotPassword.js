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
                        <center><h2 class="mb-2 mt-2" style="color: #963E97;">Forgot Password</h2></center>
                        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                            {{error}}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                        <!--<form action="/login" method="post">-->
                        <br>
                            <div class="row mb-2">
                                <div class="col-sm-12">
                                    <div class="form-group">
                                        <label>Enter your registered email:-</label>
                                        <input type="email" class="form-control form-control-sm" v-model="forgotpwd.email" required>
                                    </div>
                                </div>
                            </div>
                            <br>
                            <div class="row">
                                <div class="col-sm-12">
                                    <center>
                                        <router-link class="btn btn-outline-primary btn-sm" to="/register">Register</router-link>&nbsp;&nbsp;&nbsp;
                                        <button type="submit" class="btn btn-primary btn-sm" @click='fpwdsub'>Submit</button>
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
            forgotpwd: {
                email: null,
            },
            error: null,
        }
    },
    methods: {
        async fpwdsub(){
            const res = await fetch('/forgotpassword', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.forgotpwd), //javascript object to json
            })
            const data = await res.json();    //json string to js object
            if(res.ok){
                console.log(data);
                sessionStorage.setItem('email', data.details.email);
                sessionStorage.setItem('otp', data.details.otp);
                alert("OTP sent on registered email.");
                this.$router.push('/enterotp');
            }
            else {
                this.error = data.message;
            }
        },
    },
}