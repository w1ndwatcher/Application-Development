export default {
    template: `<div class="container" style="margin-top: 70px;">
        <h3>Welcome, {{ full_name }}!</h3>
        <div class="row mt-3 mb-3">
            <div class="col-md-12 col-sm-12">
                <div class="card">
                    <div class="card-header">Sections</div>
                    <div class="card-body">
                        <div class="row mt-2 mb-2" v-if="sections.length>0">
                            <div class="col-md-2 col-sm-6" v-for="sec in sections" :key="sec.id">
                                <div class="card mb-2">
                                    <div class="card-body">
                                        <div class="row border-bottom" style="background-color: #301934;color: white; height: 100px;">
                                            <div class="col-md-12 col-sm-12">
                                                <center><i :class="[sec.section_icon, 'fa-2x', 'mt-4']"></i></center>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-12 col-sm-12">
                                                <p><b>{{ sec.section_name }}</b><br>
                                                <span style="font-size:10pt;">{{ sec.description }}</span></p>
                                                <center>
                                                    <button class="btn btn-primary btn-sm" @click="viewEbook(sec.id)" title="View EBooks"><i class="fa fa-eye"></i></button>&nbsp;&nbsp;&nbsp;
                                                    <button class="btn btn-primary btn-sm" @click="addEbook(sec.id)" title="Add EBooks"><i class="fa fa-plus"></i></button>
                                                </center>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row mt-2 mb-2" v-else>
                            <div class="col-md-12 col-sm-12">
                                <p class="text-muted"><i>Add Sections to View</i></p>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer" v-if="sections.length>0">
                        <router-link to="/section">View All</router-link>
                    </div>
                    <div class="card-footer" v-else>
                        <router-link to="/section">Add Section</router-link>
                    </div>
                </div>
            </div>
        </div>
        <div class="row mt-3 mb-3">
            <div class="col-md-12 col-sm-12">
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
                                        <button class="btn btn-success btn-sm" @click="approve_request(bk.id)" title="Issue Ebook">Grant</button>&nbsp;&nbsp;&nbsp;
                                        <button class="btn btn-danger btn-sm" @click="reject_request(bk.id)" title="Reject Request">Reject</button>
                                    </td>
                                    <td v-if="bk.status === 'issued'">
                                        <button class="btn btn-danger btn-sm" @click="revoke_request(bk.id)" title="Revoke Access">Revoke</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="row mt-2 mb-2" v-else>
                            <div class="col-md-12 col-sm-12">
                                <p class="text-muted"><i>You have no pending requests.</i></p>
                            </div>
                        </div>
                    </div>
                    <div class="card-footer" v-if="book_requests.length>0">
                        <router-link to="/allrequests">View All</router-link>
                    </div>
                </div>
            </div>
        </div>
        <div class="row mt-3 mb-3">
            <div class="col-md-12 col-sm-12">
                <div class="card">
                    <div class="card-header">Statistics</div>
                    <div class="card-body">
                        <div class="row mt-2 mb-3">
                            <div class="col-md-3 col-sm-6">
                                <div class="card rounded-border">
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-md-8 col-sm-8">
                                                <h2 style="color: #301934;">{{ statsdata.active_users }}</h2>
                                                <p style="font-size:10pt;color: #301934;">Active Users</p>
                                            </div>
                                            <div class="col-md-4 col-sm-4">
                                                <center><i class="fa fa-user mt-3" style="color: #301934;font-size:32pt;"></i></center>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-sm-6">
                                <div class="card rounded-border">
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-md-8 col-sm-8">
                                                <h2 style="color: #301934;">{{ statsdata.grant_requests }}</h2>
                                                <p style="font-size:10pt;color: #301934;">Grant requests</p>
                                            </div>
                                            <div class="col-md-4 col-sm-4">
                                                <center><i class="fa fa-check mt-3" style="color: #301934;font-size:32pt;"></i></center>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-sm-6">
                                <div class="card rounded-border">
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-md-8 col-sm-8">
                                                <h2 style="color: #301934;">{{ statsdata.books_issued }}</h2>
                                                <p style="font-size:10pt;color: #301934;">Books Issued</p>
                                            </div>
                                            <div class="col-md-4 col-sm-4">
                                                <center><i class="fa fa-book mt-3" style="color: #301934;font-size:32pt;"></i></center>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3 col-sm-6">
                                <div class="card rounded-border">
                                    <div class="card-body">
                                        <div class="row">
                                            <div class="col-md-8 col-sm-8">
                                                <h2 style="color: #301934;">{{ statsdata.books_revoked }}</h2>
                                                <p style="font-size:10pt;color: #301934;">Revokes</p>
                                            </div>
                                            <div class="col-md-4 col-sm-4">
                                                <center><i class="fa fa-redo mt-3" style="color: #301934;font-size:32pt;"></i></center>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <br>
                        <div class="row">
                            <div class="col-md-1 col-sm-1"></div>
                            <div class="col-md-4 col-sm-12">
                                <div style="height: 290px; text-align: center;" v-if="statsdata.sections.length > 0">
                                    <canvas id="myDoughnutChart"></canvas>
                                </div>
                                <div style="height: 290px; text-align: center;" v-else>
                                    <br>
                                    <br>
                                    <p class="text-muted"><i>Add E-Books in Sections.</i></p>
                                </div>
                            </div>
                            <div class="col-md-7 col-sm-12">
                                <br>
                                <canvas id="myChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`,

    data(){
        return {
            sections: [],
            book_requests: [],
            statsdata: null,
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
            full_name: sessionStorage.getItem('full_name'),
        }
    },

    async mounted(){
        await this.fetchSections();  
        await this.fetchBookRequests();
        await this.fetchStats();

        // Chart.js setup
        const ctx = document.getElementById('myChart').getContext('2d');
        new Chart(ctx, {
        type: 'bar', // or 'line', 'pie', 'doughnut', etc.
        data: {
            labels: this.statsdata.weekdays,
            datasets: [{
            label: 'Book Issues Last Week',
            data: this.statsdata.issue_counts,
            backgroundColor: 'rgba(150, 62, 151, 0.5)',
            borderColor: 'rgba(150, 62, 151, 1)',
            borderWidth: 1
            }]
        },
        options: {
            scales: {
                x:{
                    grid: {display:false},
                },
                y: {
                    grid: {display:false},
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: "E-Books Issued in Last 7 Days"
                },
            }
        }
        });

        const ctx1 = document.getElementById('myDoughnutChart').getContext('2d');
        new Chart(ctx1, {
            type: 'doughnut', // or 'line', 'pie', 'doughnut', etc.
            data: {
                labels: this.statsdata.sections,
                datasets: [{
                    label: 'EBooks per Section',
                    data: this.statsdata.ebook_counts,
                    backgroundColor: this.statsdata.sec_colors,
                    borderColor: this.statsdata.sec_colors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: "Ebooks per Section"
                    },
                    legend: {
                        position: 'right',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return tooltipItem.label + ': ' + tooltipItem.raw;
                            }
                        }
                    }
                }
            }
            });
    },

    methods: {
        async fetchSections(){
            const secres = await fetch('/lib_section', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            })
            if (secres.status == 200) {
                const data = await secres.json();
                this.sections = data.sections;
            } else {
                const data = await secres.json(); 
                this.error = data.message;
            }
        },

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

        async fetchStats(){
            const stres = await fetch('/lib_stats', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            });
            if (stres.status == 200) {
                const data = await stres.json();
                this.statsdata = data.stats;
                console.log(this.statsdata);
            } else {
                const data = await stres.json(); 
                this.error = data.message;
            }
        },

        async approve_request(reqid){
            this.error = null;
            const data = null;
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
            this.error = null;
            const data = null;
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
            this.error = null;
            const data = null;
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

        async allsections(){
            this.$router.push({path:'/section'});
        },

        async allrequests(){
            this.$router.push({path:'/requests'});
        },

        async viewEbook(id){
            this.$router.push({path:'/viewebooks', query: {secid: id}});
        },

        async addEbook(id){
            this.$router.push({path:'/addebook', query: {secid: id}});
        }
    }

}