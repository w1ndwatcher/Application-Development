export default {
    template: `
    <div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header">Book Requests</div>
            <div class="card-body">
                <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{error}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                <table id="allsections" class="table table-striped" style="width:100%" v-if="book_requests.length>0">
                    <thead>
                        <tr>
                            <th>Book Name</th>
                            <th>Author</th>
                            <th>User</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="bk in book_requests" :key="bk.id">
                            <td>{{ bk.book_name }}</td>
                            <td>{{ bk.author }}</td>
                            <td>{{ bk.user_name }}</td>
                            <td v-if="bk.status === 'requested'">
                                <button class="btn btn-primary btn-sm" @click="viewEbook(bk.bookid)" title="View Ebook">View</button>&nbsp;&nbsp;&nbsp;
                                <button class="btn btn-success btn-sm" @click="approve_request(bk.id)" title="Issue Ebook">Grant</button>&nbsp;&nbsp;&nbsp;
                                <button class="btn btn-danger btn-sm" @click="reject_request(bk.id)" title="Reject Request">Reject</button>
                            </td>
                            <td v-if="bk.status === 'issued'">
                                <button class="btn btn-primary btn-sm" @click="viewEbook(bk.bookid)" title="View Ebook">View</button>&nbsp;&nbsp;&nbsp;
                                <button class="btn btn-danger btn-sm" @click="revoke_request(bk.id)" title="Revoke Access">Revoke</button>
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
            book_requests: [],
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
            isWaiting: false,
        }
    },

    async mounted(){ 
        await this.fetchBookRequests();
    },

    methods: {
        async fetchBookRequests(){
            const bkreqres = await fetch('/lib_bookrequests', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            });
            if (bkreqres.status == 200) {
                const data = await bkreqres.json();
                this.book_requests = data.book_requests;
            } else {
                const data = await bkreqres.json(); 
                this.error = data.message;
            }
        },

        async approve_request(reqid){
            if (confirm('Approve Request?')){
                const res = await fetch(`/approve_request?reqid=${reqid}`, {
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

        async reject_request(reqid){
            if (confirm('Reject Request?')){
                const res = await fetch(`/reject_request?reqid=${reqid}`, {
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

        async revoke_request(reqid){
            if (confirm('Are you sure you want to revoke access to this book?')){
                const res = await fetch(`/revoke_access?reqid=${reqid}`, {
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

        async viewEbook(id){
            this.$router.push({path:'/read_ebook', query: {bookid: id}});
        },
    }
}