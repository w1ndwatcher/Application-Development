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
                <div class="row mt-2 mb-3" v-if="issues_history.length>0">
                    <div class="col-md-12 col-sm-12 text-end">
                        <button class="btn btn-primary btn-sm" @click='downloadResource'>Download Report</button>
                        <span v-if='isWaiting'>&nbsp;Waiting...</span>
                    </div>
                </div>
                <div class="table-responsive" v-if="issues_history.length>0">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Section</th>
                                <th>Book Name</th>
                                <th>Status</th>
                                <th>Issued By</th>
                                <th>Requested On</th>
                                <th>Issued On</th>
                                <th>Returned On</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="bk in issues_history" :key="bk.id">
                                <td>{{ bk.section_name }}</td>
                                <td>{{ bk.book_name }}</td>
                                <td>{{ bk.status }}</td>
                                <td>{{ bk.full_name }}</td>
                                <td>{{ bk.request_on }}</td>
                                <td>{{ bk.issue_date }}</td>
                                <td>{{ bk.returned_on }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
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
            issues_history: [],
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
            const bkreqres = await fetch('/issue_history', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            });
            if (bkreqres.status == 200) {
                const data = await bkreqres.json();
                this.issues_history = data.issues_history;
            } else {
                const data = await bkreqres.json(); 
                this.error = data.message;
            }
        },

        async downloadResource(){
            this.isWaiting = true;
            const res = await fetch('/download-csv');
            const data = await res.json();
            if(res.ok){
                const taskId = data["task-id"];
                const intv = setInterval(async() => {
                    const csv_res = await fetch(`/get-csv/${taskId}`);
                    if (csv_res.ok){
                        this.isWaiting = false;
                        clearInterval(intv);
                        window.location.href = `/get-csv/${taskId}`
                    }
                }, 1000)
            }
        },
    }
}