export default {
    template:
    `<div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header">My Ebooks</div>
            <div class="card-body">
                <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{error}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                <table id="allsections" class="table table-striped" style="width:100%" v-if="issued_ebooks.length>0">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Author</th>
                            <th>Section</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="bk in issued_ebooks" :key="bk.id">
                            <td>{{ bk.book_name }}</td>
                            <td>{{ bk.author }}</td>
                            <td>{{ bk.section_name }}</td>
                            <td v-if="bk.status == 'issued'">
                                <button class="btn btn-primary btn-sm" @click="readEBook(bk.id)" title="Read EBook">Read</button>&nbsp;&nbsp;&nbsp;
                                <button class="btn btn-outline-primary btn-sm" @click="returnEBook(bk.id)" title="Return EBook">Return</button>
                            </td>
                            <td v-if="bk.status == 'rejected'">
                                <span class="text-danger">Rejected</span>
                            </td>
                            <td v-if="bk.status == 'requested'">
                                <span class="text-success">Requested</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="row mt-2 mb-2" v-else>
                    <div class="col-md-12 col-sm-12">
                        <p class="text-muted text-center"><i>No Requests made yet.</i></p>
                    </div>
                </div>
            </div>
        </div>
    </div>`,

    data(){
        return {
            issued_ebooks: [],
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
        }
    },

    async mounted(){
        await this.fetchmyEBooks();  
    },

    methods: {
        async fetchmyEBooks(){
            const bkres = await fetch(`/my_ebooks`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            })
            if (bkres.status == 200) {
                const data = await bkres.json();
                this.issued_ebooks = data.issued_books;
            } else {
                const data = await bkres.json(); 
                this.error = data.message;
            }
        },

        async readEBook(id){
            this.$router.push({path:'/read_ebook', query: {bookid: id}});
        },

        async returnEBook(id){ 
            if (confirm('Are you sure you want to return this book?')){
                const res = await fetch(`/return_ebook?bookid=${id}`, {
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
    },
}