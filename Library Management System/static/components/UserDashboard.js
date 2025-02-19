export default {
    template: 
    `<div class="container" style="margin-top: 70px;">
        <h3>Welcome, {{ full_name }}!</h3>
        <div class="row mt-3 mb-3">
            <div class="col-md-12 col-sm-12">
                <div class="card">
                    <div class="card-header">Search Ebook</div>
                    <div class="card-body">
                        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                            {{error}}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                        <div class="row">
                            <div class="col-md-6 col-sm-12">
                                <div class="form-group">
                                    <input type="text" class="form-control form-control-sm" name="param" v-model="query" @input="searchInput" placeholder="Search by section, author or title...">
                                </div>
                            </div>
                            <!--<div class="col-md-4 col-sm-2">
                                <button class="btn btn-primary btn-sm" @click="search"><i class="fa fa-search"></i>&nbsp;&nbsp;Search</button>&nbsp;&nbsp;&nbsp;
                                <button class="btn btn-outline-primary btn-sm" @click="clear"><i class="fa fa-redo"></i>&nbsp;&nbsp;Clear</button>
                            </div>-->
                        </div>
                        <br>
                        <div class="table-responsive">
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
                                        <td>
                                            <span class="text-success" v-if="bk.status == 'requested' || bk.status == 'issued'">{{ bk.status }}</span>
                                            <button v-else class="btn btn-outline-primary btn-sm" @click="reqEBook(bk.id)" title="Request EBook">Request</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="table-responsive">
                            <table id="allsections" v-if="results.sections.length>0" class="table table-striped" style="width:100%">
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
                        </div>
                        <p v-if="results.msg">{{ results.msg }}</p>
                    </div>
                    <div class="card-footer">
                        <router-link to="/usersections">View All</router-link>
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
                            <div class="col-md-6 col-sm-12">
                                <div class="row mt-3 mb-3">
                                    <div class="col-md-6 col-sm-12">
                                        <div class="card rounded-border">
                                            <div class="card-body">
                                                <div class="row">
                                                    <div class="col-md-8 col-sm-8">
                                                        <h2 style="color: #301934;">{{ statsdata.books_read }}</h2>
                                                        <p style="font-size:10pt;color: #301934;">Books Read</p>
                                                    </div>
                                                    <div class="col-md-4 col-sm-4">
                                                        <center><i class="fa fa-book mt-3" style="color: #301934;font-size:32pt;"></i></center>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6 col-sm-12">
                                        <div class="card rounded-border">
                                            <div class="card-body">
                                                <div class="row">
                                                    <div class="col-md-8 col-sm-8">
                                                        <h2 style="color: #301934;">{{ statsdata.books_requested }}</h2>
                                                        <p style="font-size:10pt;color: #301934;">Books Requested</p>
                                                    </div>
                                                    <div class="col-md-4 col-sm-4">
                                                        <center><i class="fa fa-list mt-3" style="color: #301934;font-size:32pt;"></i></center>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="row mt-3 mb-3">
                                    <div class="col-md-6 col-sm-12">
                                        <div class="card rounded-border">
                                            <div class="card-body">
                                                <div class="row">
                                                    <div class="col-md-8 col-sm-8">
                                                        <h2 style="color: #301934;">{{ statsdata.books_issued }}</h2>
                                                        <p style="font-size:10pt;color: #301934;">Books Issued</p>
                                                    </div>
                                                    <div class="col-md-4 col-sm-4">
                                                        <center><i class="fa fa-check mt-3" style="color: #301934;font-size:32pt;"></i></center>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6 col-sm-12">
                                        <div class="card rounded-border">
                                            <div class="card-body">
                                                <div class="row">
                                                    <div class="col-md-8 col-sm-8">
                                                        <h2 style="color: #301934;">{{ statsdata.ebooks_rejected }}</h2>
                                                        <p style="font-size:10pt;color: #301934;">Rejected</p>
                                                    </div>
                                                    <div class="col-md-4 col-sm-4">
                                                        <center><i class="fa fa-redo mt-3" style="color: #301934;font-size:32pt;"></i></center>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-1 col-sm-1"></div>
                            <div class="col-md-5 col-sm-12">
                                <div style="height: 290px; text-align: center;" v-if="statsdata.sections.length>0">
                                    <canvas id="myDoughnutChart"></canvas>
                                </div>
                                <div style="height: 290px; text-align: center;" v-else>
                                    <br>
                                    <br>
                                    <br>
                                    <p class="text-muted"><i>You can read E-Books from different Sections.</i></p>
                                </div>
                            </div>
                        </div>
                        <br>
                        <div class="row">
                            <div class="col-md-12 col-sm-12" v-if="statsdata.avg_ratings.length>0">
                                <canvas id="myChart"></canvas>
                            </div>
                            <div class="col-md-12 col-sm-12" style="text-align: center;" v-else>
                                <br>
                                <br>
                                <p class="text-muted text-center"><i>Rate E-Books to let people know what you like.</i></p>
                            </div>
                        </div>
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
            statsdata: null,
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
            full_name: sessionStorage.getItem('full_name'),
        }
    },

    async mounted(){
        await this.fetchStats();

        // Chart.js setup
        const ctx1 = document.getElementById('myDoughnutChart').getContext('2d');
        if (ctx1){
            new Chart(ctx1, {
                type: 'doughnut', 
                data: {
                    labels: this.statsdata.sections,
                    datasets: [{
                        label: 'EBooks Read per Section',
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
                            text: "No. of books read in different Sections"
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
        }

        const ctx = document.getElementById('myChart').getContext('2d');
        if (ctx){
            new Chart(ctx, {
            type: 'bar', 
            data: {
                labels: this.statsdata.book_names,
                datasets: [{
                label: 'Top Rated Ebooks',
                data: this.statsdata.avg_ratings,
                backgroundColor: 'rgba(150, 62, 151, 0.5)',
                borderColor: 'rgba(150, 62, 151, 1)',
                borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                scales: {
                    x: {
                        grid: {display:false},
                        beginAtZero: true,
                        max: 5
                    },
                    y:{
                        grid: {display:false},
                    },
                },
                plugins: {
                    title: {
                        display: true,
                        text: "Top 5 Rated E-Books"
                    },
                }
            }
            });
        }
    },

    methods: {
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
                    // this.$router.push({path:'/mybooks'});
                    const data = await reqres.json();
                    alert(data.message);
                    window.location.reload();
                } else {
                    const data = await reqres.json(); 
                    this.error = data.message;
                }
            }
        },

        async viewEbook(id){
            this.$router.push({path:'/viewebooks', query: {secid: id}});
        },

        // async search(){
        //     const res = await fetch(`/search?query=${this.query}`, {
        //         method: 'GET',
        //         headers: {
        //             'Content-Type': 'application/json',
        //             'Authentication-Token': this.token,
        //         },
        //     });
        //     if (res.status == 200) {
        //         const data = await res.json();
        //         if (data.results){
        //             if (data.results.books){
        //                 this.results.books = data.results.books;
        //             }
        //             if (data.results.sections) {
        //                 this.results.sections = data.results.sections;
        //             }
        //         } else {
        //             this.results.msg = data.message;
        //         }
        //     } else {
        //         const data = await res.json(); 
        //         this.error = data.message;
        //     }
        // },

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

        // async clear(){
        //     window.location.reload();
        // },

        async gotosections(){
            this.$router.push({path:'/usersections'});
        },

        async fetchStats(){
            const stres = await fetch('/user_stats', {
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
    },
}