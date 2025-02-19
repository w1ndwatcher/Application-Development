export default {
    template:
    `<div class="container" style="margin-top: 70px;">
        <div class="card">
            <div class="card-header">Add Section</div>
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
                                <option value="fas fa-microscope">Microscope</option>
                                <option value="fas fa-vial">Vial</option>
                                <option value="fas fa-magnet">Magnet</option>
                                <option value="fas fa-pills">Pills</option>
                                <option value="fas fa-laptop-code">Laptop</option>
                                <option value="fas fa-robot">Robot</option>
                                <option value="fa fa-plus">Plus</option>
                                <option value="fas fa-donate">Currency</option>
                                <option value="fas fa-line-chart">Line Chart</option>
                                <option value="fas fa-landmark">Monument</option>
                                <option value="fas fa-galactic-republic">Republic</option>
                                <option value="fas fa-palette">Palette</option>
                                <option value="fas fa-language">Alphabet</option>
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
                        <button type="submit" class="btn btn-primary btn-sm mt-4" @click='addsection'>Submit</button>
                    </div>
                </div>
            </div>
        </div>
        <br>
        <div class="card">
            <div class="card-header">Sections</div>
            <div class="card-body">
                <table id="allsections" class="table table-striped" style="width:100%" v-if="sections.length>0">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Icon</th>
                            <th>Description</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="sec in sections" :key="sec.id">
                            <td>{{ sec.section_name }}</td>
                            <td><i :class="sec.section_icon"></i></td>
                            <td>{{ sec.description }}</td>
                            <td>
                                <button class="btn btn-outline-primary btn-sm" @click="gotoEbook(sec.id)" data-toggle="tooltip" data-placement="top" title="Add Ebook"><i class="fa fa-plus"></i></button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                <button class="btn btn-outline-primary btn-sm" @click="viewEbook(sec.id)" title="View EBooks"><i class="fa fa-eye"></i></button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                <button class="btn btn-outline-primary btn-sm" @click="gotoEditSec(sec.id)" title="Edit Section"><i class="fa fa-edit"></i></button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                <button class="btn btn-outline-danger btn-sm" @click="deleteSection(sec.id)" title="Delete Section"><i class="fa fa-trash"></i></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div class="row mt-2 mb-2" v-else>
                    <div class="col-md-12 col-sm-12">
                        <p class="text-muted text-center"><i>Add Sections to View</i></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,

    data(){
        return {
            secdetail: {
                "section_name": null,
                "section_icon": null,
                "description": null,
                "id": null,
            },
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
        async addsection(){
            if (this.secdetail.section_name == null) {
                this.error = "Section name is mandatory!";
                return;
            } else {
                const res = await fetch('/api/manage_section', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': this.token,
                    },
                    body: JSON.stringify(this.secdetail),
                });
                if(res.ok){
                    const data = await res.json(); 
                    console.log(data);
                    alert(data.message);
                    window.location.reload();
                } else {
                    const data = await res.json(); 
                    this.error = data.message;
                }
            } 
        },

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

        gotoEditSec(id) {
            this.$router.push({path:'/editsection', query: {secid: id}});
        },

        async gotoEbook(id){
            this.$router.push({path:'/addebook', query: {secid: id}});
        },

        async viewEbook(id){
            this.$router.push({path:'/viewebooks', query: {secid: id}});
        },

        async deleteSection(id){
            if (confirm('Are you sure you want to delete this section?')){
                const res = await fetch(`/api/manage_section?secid=${id}`, {
                    method: 'DELETE',
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