export default {
    template:
    `<div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header"><router-link class="fa fa-angle-left back-link" to="/section"></router-link> Add Ebook</div>
            <div class="card-body">
                <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{error}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <div class="form-group">
                            <label>Title</label>
                            <input type="text" class="form-control form-control-sm" name="ebtitle" v-model="bookdetails.book_name" required>
                        </div>
                    </div>
                </div>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <div class="form-group">
                            <label>Author</label>
                            <input type="text" class="form-control form-control-sm" name="ebauthor" v-model="bookdetails.author" required>
                        </div>
                    </div>
                </div>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <div class="form-group">
                            <label>Content</label>
                            <!--<div id="editor" v-model="bookdetails.content"></div>-->
                            <textarea rows="15" class="form-control form-control-sm" name="ebcontent" v-model="bookdetails.content" required></textarea>
                        </div>
                    </div>
                </div>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <button type="submit" class="btn btn-primary btn-sm" @click='addbook'>Submit</button>
                    </div>
                </div>
            </div>
        </div>
    </div>`,

    data(){
        return {
            bookdetails: {
                "section_id": null,
                "book_name": null,
                "author": null,
                "content": null,
            },
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
        }
    },

    created() {
        this.bookdetails.section_id = this.$route.query.secid;
    },

    methods: {
        async addbook(){
            if (this.bookdetails.book_name == null || this.bookdetails.author == null || this.bookdetails.content == null) {
                this.error = "All fields are mandatory!";
                return;
            } else {
                const res = await fetch('/addebook', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.token,
                    },
                    body: JSON.stringify(this.bookdetails),
                });
                if(res.ok){
                    const data = await res.json(); 
                    const secid = this.bookdetails.section_id;
                    alert("E-Book added successfully!");
                    this.$router.push({path:'/viewebooks', query: {secid: secid}});
                } else {
                    const data = await res.json(); 
                    this.error = data.message;
                }
            }
        }
    },
}