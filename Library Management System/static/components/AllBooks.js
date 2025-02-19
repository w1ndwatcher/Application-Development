export default {
    template:
    `<div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header">Search Ebook</div>
            <div class="card-body">
                <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{error}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                <div class="row">
                    <div class="col-md-6 col-sm-8">
                        <div class="form-group">
                            <input type="text" class="form-control form-control-sm" name="param" v-model="query" @input="searchInput" placeholder="Search by section, author or title...">
                        </div>
                    </div>
                </div>
                <br>
                <table id="allsections" v-if="results.books.length>0" class="table table-striped" style="width:100%">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Author</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="bk in results.books" :key="bk.id">
                            <td>{{ bk.book_name }}</td>
                            <td>{{ bk.author }}</td>
                            <td v-if="role=='general_user'">
                                <span class="text-success" v-if="bk.status == 'requested' || bk.status == 'issued'">{{ bk.status }}</span>
                                <button v-else class="btn btn-outline-primary btn-sm" @click="reqEBook(bk.id)" title="Request EBook">Request</button>
                            </td>
                            <td v-if="role=='librarian'">
                                <button class="btn btn-outline-primary btn-sm" @click="editEBook(bk.id)" title="View/Edit EBook"><i class="fa fa-eye"></i></button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                <button class="btn btn-outline-danger btn-sm" @click="deleteEBook(bk.id)" title="Delete EBook"><i class="fa fa-trash"></i></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <table id="allsections" v-if="results.sections.length>0" class="table table-striped table-responsive" style="width:100%">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="sec in results.sections" :key="sec.id">
                            <td>{{ sec.section_name }}</td>
                            <td>{{ sec.description }}</td>
                            <td>
                                <button class="btn btn-outline-primary btn-sm" @click="viewEbook(sec.id)" title="View EBooks">View Books</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p v-if="results.msg">{{ results.msg }}</p>
            </div>
        </div>
        <br>
        <div class="card">
            <div class="card-header">
                All EBooks
            </div>
            <div class="card-body">
                <table id="allsections" class="table table-striped table-responsive" style="width:100%" v-if="ebooks.length>0">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Author</th>
                            <th>Section</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="bk in ebooks" :key="bk.id">
                            <td>{{ bk.book_name }}</td>
                            <td>{{ bk.author }}</td>
                            <td>{{ bk.section_name }}</td>
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
            query: "",
            results: {
                books: [],
                sections: [],
                msg: null,
            },
            ebooks: [],
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
        }
    },

    async mounted(){
        await this.fetchEBooks();  
    },

    methods: {
        async searchInput(){
            console.log(this.query);
            if (this.query.trim() === "") {
                this.results = {
                    books: [],
                    sections: [],
                    msg: null,
                };
                return;
            }
            const res = await fetch(`/search?query=${this.query}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            });
            if (res.status == 200) {
                const data = await res.json();
                if (data.results){
                    if (data.results.books){
                        this.results.books = data.results.books;
                    }
                    if (data.results.sections) {
                        this.results.sections = data.results.sections;
                    }
                } else {
                    this.results.msg = data.message;
                }
            } else {
                const data = await res.json(); 
                this.error = data.message;
            }
        },


        async fetchEBooks(){
            const bkres = await fetch(`/all_ebooks`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            })
            if (bkres.status == 200) {
                const data = await bkres.json();
                this.ebooks = data.ebooks;
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
                    alert(data.message);
                    window.location.reload();
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
                    alert(data.message);
                    window.location.reload();
                }
            }
        },
    },

}