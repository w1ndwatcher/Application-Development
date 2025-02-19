export default {
    template:
    `<div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header">Sections</div>
            <div class="card-body">
                <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{error}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                <div class="row mt-2 mb-2" v-if="sections.length>0">
                    <div class="col-md-2 col-sm-6" v-for="sec in sections" :key="sec.id">
                        <div class="card mb-3">
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
                                            <button class="btn btn-primary btn-sm" @click="viewEbook(sec.id)" title="View EBooks"><i class="fa fa-eye"></i></button>
                                        </center>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row mt-2 mb-2" v-else>
                    <div class="col-md-12 col-sm-12">
                        <p class="text-muted text-center"><i>No Sections added yet.</i></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,

    data(){
        return {
            sections: [],
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
        }
    },

    async mounted(){
        await this.fetchSections();  
    },

    methods: {
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

        async viewEbook(id){
            this.$router.push({path:'/viewebooks', query: {secid: id}});
        },
    },
}