export default {
    template:`
    <div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header">
                <h3>
                    <router-link class="fa fa-angle-left back-link" v-if="role=='general_user'" to="/mybooks"></router-link> 
                    <router-link class="fa fa-angle-left back-link" v-if="role=='librarian'" to="/allrequests"></router-link> 
                    {{ book_data.book_name }}
                </h3>
                <p>{{ book_data.author }}</p>
                <p>({{ book_data.section_name }})</p>
            </div>
            <div class="card-body">
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <div style="height: 300px; overflow-y: scroll; text-align: justify; font-size: 14px; line-height:2;">{{ book_data.content }}</div>
                    </div>
                </div>
            </div>
        </div>
        <br>
        <div class="card" v-if="role==='general_user'">
            <div class="card-header">
                Rate Ebook
            </div>
            <div class="card-body">
                <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{error}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <div class="rating">
                            <input type="radio" id="star5" name="rating" value="5" v-model="rating_details.value" :checked="rating_details.value == 5">
                            <label for="star5">&#9733;</label>
                            <input type="radio" id="star4" name="rating" value="4" v-model="rating_details.value" :checked="rating_details.value == 4">
                            <label for="star4">&#9733;</label>
                            <input type="radio" id="star3" name="rating" value="3" v-model="rating_details.value" :checked="rating_details.value == 3">
                            <label for="star3">&#9733;</label>
                            <input type="radio" id="star2" name="rating" value="2" v-model="rating_details.value" :checked="rating_details.value == 2">
                            <label for="star2">&#9733;</label>
                            <input type="radio" id="star1" name="rating" value="1" v-model="rating_details.value" :checked="rating_details.value == 1">
                            <label for="star1">&#9733;</label>
                        </div>
                    </div>
                </div>
                <div class="row mb-2">
                    <div class="col-md-12 col-sm-12">
                        <button type="submit" class="btn btn-primary btn-sm" @click='ratebook'>Submit</button>
                    </div>
                </div>
            </div>
        </div>
        <br>
    </div>`,

    data(){
        return {
            bookid: null,
            book_data: null,
            rating_details: {
                "value": 0,
                "bookid": null,
            },
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
           
        }
    },

    created() {
        this.bookid = this.$route.query.bookid;
        this.rating_details.bookid = this.$route.query.bookid;
    },

    async mounted(){
        await this.fetchEBook();  
        await this.fetchRating();
        console.log(this.token);
    },

    methods: {
        async fetchEBook(){
            const bkres = await fetch(`/read_ebook?bookid=${this.bookid}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            })
            if (bkres.status == 200) {
                const data = await bkres.json();
                this.book_data = data.book_data;
            } else {
                const data = await bkres.json(); 
                this.error = data.message;
            }
        },

        async fetchRating(){
            const rateres = await fetch(`/getrating?bookid=${this.bookid}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            })
            if (rateres.status == 200) {
                const data = await rateres.json();
                this.rating_details.value = data.rating;
                console.log(this.rating_details.value);
            } else {
                const data = await rateres.json(); 
                this.error = data.message;
            }
        },

        async ratebook(){
            if (this.rating==0){
                this.error = "Please select rating from 1 to 5!";
                return;
            } else {
                const res = await fetch(`/rateebook?bookid=${this.bookid}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.token,
                    },
                    body: JSON.stringify(this.rating_details),
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
        }
    },
}