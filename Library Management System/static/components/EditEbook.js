export default {
    template:
    `<div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header"><router-link class="fa fa-angle-left back-link" :to="'/viewebooks?secid=' + bookdetails.section_id"></router-link> Edit Ebook</div>
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
                            <label>Section</label>
                            <select class="form-control form-control-sm" name="ebsec" v-model="bookdetails.section_id" required>
                                <option :value="bookdetails.section_id">{{ bookdetails.section_name }}</option>
                                <option v-for="sec in sections" :key="sec.id" :value="sec.id">{{ sec.section_name }}</option>
                            </select>
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
                            <textarea rows="15" class="form-control form-control-sm" name="ebcontent" v-model="bookdetails.content" required></textarea>
                        </div>
                    </div>
                </div>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <button type="submit" class="btn btn-primary btn-sm" @click='editbook'>Save Changes</button>
                    </div>
                </div>
            </div>
        </div>
    </div>`,

    data(){
        return {
            bookid: null,
            sections: [],
            bookdetails: {
                "section_id": null,
                "section_name":null,
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
        this.bookid = this.$route.query.bookid;
        console.log(this.bookid);
    },

    async mounted(){
        await this.fetchSections();  
        await this.fetchEbook(); 
    },

    methods: {
        async fetchEbook(){
            const bkres = await fetch(`/read_ebook?bookid=${this.bookid}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            })
            if (bkres.status == 200) {
                const data = await bkres.json();
                this.bookdetails.book_name = data.book_data.book_name;
                this.bookdetails.author = data.book_data.author;
                this.bookdetails.content = data.book_data.content;
                this.bookdetails.section_id = data.book_data.section_id;
                this.bookdetails.section_name = data.book_data.section_name;
            } else {
                const data = await bkres.json(); 
                this.error = data.message;
            }
        },

        async fetchSections(){
            const secres = await fetch('/api/manage_section', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            })
            if (secres.status == 200) {
                const data = await secres.json();
                this.sections = data;
            } else {
                const data = await secres.json(); 
                this.error = data.message;
            }
        },

        async editbook(){
            if (this.bookdetails.book_name == null || this.bookdetails.author == null || this.bookdetails.content == null) {
                this.error = "All fields are mandatory!";
                return;
            } else {
                const res = await fetch(`/editebook?bookid=${this.bookid}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.token,
                    },
                    body: JSON.stringify(this.bookdetails),
                });
                if(res.ok){ 
                    const data = await res.json(); 
                    alert(data.message);
                    window.location.reload();
                } else {
                    const data = await res.json(); 
                    this.error = data.message;
                }
            }
        },
    }
}