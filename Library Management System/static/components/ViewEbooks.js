export default {
    template:
    `<div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header">
                <router-link class="fa fa-angle-left back-link" v-if="role=='general_user'" to="/usersections"></router-link> 
                <router-link class="fa fa-angle-left back-link" v-if="role=='librarian'" to="/section"></router-link> 
                EBooks under {{ section_name }}
            </div>
            <div class="card-body">
                <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{error}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                <table id="allsections" class="table table-striped" style="width:100%" v-if="ebooks.length>0">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Author</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="bk in ebooks" :key="bk.id">
                            <td>{{ bk.book_name }}</td>
                            <td>{{ bk.author }}</td>
                            <td v-if="role=='librarian'">
                                <button class="btn btn-outline-primary btn-sm" @click="editEBook(bk.id)" title="View/Edit EBook"><i class="fa fa-eye"></i></button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                <button class="btn btn-outline-danger btn-sm" @click="deleteEBook(bk.id)" title="Delete EBook"><i class="fa fa-trash"></i></button>
                            </td>
                            <td v-if="role=='general_user'">
                                <span class="text-success" v-if="bk.status == 'requested' || bk.status == 'issued'">{{ bk.status }}</span>
                                <button v-else class="btn btn-outline-primary btn-sm" @click="reqEBook(bk.id)" title="Request EBook">Request</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="row mt-2 mb-2" v-else>
                    <div class="col-md-12 col-sm-12">
                        <p class="text-muted text-center"><i>No E-Books added.</i></p>
                    </div>
                </div>
            </div>
        </div>
    </div>`,

    data(){
        return {
            section_id: null,
            section_name: null,
            ebooks: [],
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
        }
    },

    created() {
        this.section_id = this.$route.query.secid;
    },

    async mounted(){
        await this.fetchEBooks();  
        const role = this.role;
        console.log(role);
    },

    methods: {
        async fetchEBooks(){
            const bkres = await fetch(`/ebooks?section_id=${this.section_id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            })
            if (bkres.status == 200) {
                const data = await bkres.json();
                this.ebooks = data[0].ebooks;
                this.section_name = data[1].section_name;
            } else {
                const data = await bkres.json(); 
                this.error = data.message;
            }
        },

        async editEBook(id){
            this.$router.push({path:'/editebook', query: {bookid: id}});
        },

        async deleteEBook(id){
            if (confirm('Are you sure you want to delete this book?')){
                const res = await fetch(`/deleteebook?bookid=${id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.token,
                    },
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

        async reqEBook(id){
            if (confirm('Request this book?')){
                const reqres = await fetch(`/request_ebook?bookid=${id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.token,
                    },
                });
                if(reqres.ok){
                    const data = await reqres.json(); 
                    alert(data.message);
                    window.location.reload();
                } else {
                    const data = await reqres.json(); 
                    this.error = data.message;
                }
            }
        },
    },

}