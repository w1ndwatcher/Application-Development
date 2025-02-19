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
                        <center><h2 class="mb-2 mt-2" style="color: #963E97;">Set New Password</h2></center>
                        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                            {{error}}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                        <div class="row mb-2">
                            <div class="col-sm-12">
                                <div class="form-group">
                                    <label for="loginpass">Password</label>
                                    <input type="password" name="password" id="loginpass" class="form-control form-control-sm" v-model="newdetails.newpassword" required> 
                                </div>
                                <p class="text-danger" v-if="pwderror">{{ pwderror }}</p>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-sm-12">
                                <div class="form-group">
                                    <label for="logincpass">Confirm Password</label>
                                    <input type="password" name="cpassword" id="logincpass" class="form-control form-control-sm" v-model="cpassword" required> 
                                </div>
                                <p class="text-danger" v-if="cpwderror">{{ cpwderror }}</p>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm-12">
                                <center>
                                    <router-link class="btn btn-outline-primary btn-sm" to="/register">Register</router-link>&nbsp;&nbsp;&nbsp;
                                    <button type="submit" class="btn btn-primary btn-sm" @click='resetpwd'>Submit</button>
                                </center>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-3 col-sm-1"></div>
        </div>
    </div>`,
    data(){
        return {
            newdetails: {
                email: sessionStorage.getItem('email'),
                newpassword: null,
            },
            cpassword: null,
            error: null,
            pwderror: null,
            cpwderror: null
        }
    },
    methods: {
        async resetpwd(){
            this.error = null;
            this.pwderror = null;
            this.cpwderror = null;

            if (this.newdetails.newpassword.length < 6) {
                this.pwderror = "Password should be at least 6 characters!";
            } else if (this.newdetails.newpassword != this.cpassword){
                this.pwderror = "Password and Confirm password do not match!";
                this.cpwderror = "Password and Confirm password do not match!";
            } else {
                const res = await fetch('/resetpwd', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.newdetails), //javascript object to json
                })
                const data = await res.json();    //json string to js object
                if(res.ok){
                    sessionStorage.removeItem('otp')
                    alert("Password reset successfully! Proceed to Login.")
                    this.$router.push('/');
                }
                else {
                    this.error = data.message;
                }
            }
        },
    },
}