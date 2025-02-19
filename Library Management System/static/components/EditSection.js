export default {
    template:
    `<div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header"><router-link class="fa fa-angle-left back-link" to="/section"></router-link> Edit Section</div>
            <div class="card-body">
                <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
                    {{error}}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                <div class="row mb-2">
                    <div class="col-md-3 col-sm-6">
                        <div class="form-group">
                            <label for="secname">Name</label>
                            <input type="text" name="section_name" id="secname" class="form-control form-control-sm" v-model="secdetail.section_name" required> 
                        </div>
                    </div>
                    <div class="col-md-2 col-sm-6">
                        <div class="form-group">
                            <label for="secicon">Icon</label>
                            <select name="section_icon" id="secicon" class="form-control form-control-sm" v-model="secdetail.section_icon" required>
                                <option :value="secdetail.section_icon">{{ getLastWord() }}</option>
                                <option value="fas fa-microscope">Microscope</option>
                                <option value="fas fa-vial">Vial</option>
                                <option value="fas fa-magnet">Magnet</option>
                                <option value="fas fa-pills">Pills</option>
                                <option value="fas fa-laptop-code">Code</option>
                                <option value="fas fa-robot">Robot</option>
                                <option value="fa fa-plus">Plus</option>
                                <option value="fas fa-donate">Currency</option>
                                <option value="fas fa-line-chart">Chart</option>
                                <option value="fas fa-landmark">Landmark</option>
                                <option value="fas fa-galactic-republic">Republic</option>
                                <option value="fas fa-palette">Palette</option>
                                <option value="fas fa-language">Language</option>
                                <option value="fass fa-child">Child</option>
                                <option value="fas fa-volleyball-ball">Ball</option>
                                <option value="fa fa-book">Book</option>
                            </select> 
                        </div>
                    </div>
                    <div class="col-md-5 col-sm-12">
                        <div class="form-group">
                            <label for="secdesc">Description</label>
                            <textarea name="desc" id="secdesc" class="form-control form-control-sm" rows="1" v-model="secdetail.description"></textarea> 
                        </div>
                    </div>
                    <div class="col-md-2 col-sm-3">
                        <button type="submit" class="btn btn-primary btn-sm mt-4" @click='editSection()'>Submit</button>
                    </div>
                </div>
            </div>
        </div>
    </div>`,

    data(){
        return {
            secdetail: {
                section_name: null,
                section_icon: null,
                description: null
            },
            section_id: null,
            error: null,
            token: sessionStorage.getItem('auth-token'),
            role: sessionStorage.getItem('role'),
        }
    },

    created() {
        this.section_id = this.$route.query.secid;
        console.log(this.section_id);
    },

    async mounted(){
        await this.fetchSection();  
    },

    methods: {
        async fetchSection(){
            const secres = await fetch(`/getsection?secid=${this.section_id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': this.token,
                },
            })
            if (secres.status == 200) {
                const data = await secres.json();
                console.log(data);
                this.secdetail.section_name = data.section_data.section_name;
                this.secdetail.section_icon = data.section_data.icon;
                this.secdetail.description = data.section_data.desc;
                console.log(this.secdetail);
            } else {
                const data = await secres.json(); 
                this.error = data.message;
            }
        },

        getLastWord() {
            const icon = this.secdetail.section_icon;
            if(icon){
                const parts = icon.split('-');
                const lastWord = parts[parts.length - 1];
                console.log(lastWord.charAt(0).toUpperCase() + lastWord.slice(1));
                return lastWord.charAt(0).toUpperCase() + lastWord.slice(1);
            } else {
                return "No icon selected";
            }
        },

        async editSection(){
            if (this.secdetail.section_name == null) {
                this.error = "Section name is mandatory!";
                return;
            } else {
                const res = await fetch(`/api/manage_section?secid=${this.section_id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.token,
                    },
                    body: JSON.stringify(this.secdetail),
                });
                if(res.ok){ 
                    alert("Section edited successfully!");
                    this.$router.push({path:'/section'});
                } else {
                    const data = await res.json(); 
                    this.error = data.message;
                }
            } 
        },
    }
}