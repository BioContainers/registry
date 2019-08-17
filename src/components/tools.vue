<template>
  <div class="index-container">
      <div class="banner">
          <div class="content-wrapper">
              <h1 class="title">BioContainers</h1>
              <p class="description">Bioinformatics more accessible and reproducible</p> 
          </div>
      </div>
      <div class="triangle triangle-down"></div>
      <div class="content">
          <div class="container-wrapper">
            <VulnerabilitiesModal/>
            <Row :gutter="16">
                 <Col span="20">
                      <div class="title-container">
                            <div class="title-wrapper">
                                <div class="card-title">
                                    <p><strong>Tool</strong>: {{containerObj.name}}</p>
                                    <p><strong>Description</strong>: {{containerObj.description}}</p>
                                    <p class="license-wrapper"><strong>License</strong>:  <img class="license-img" :src="containerObj.license"/></p>
                                    <!--<p>Home: {{containerObj.url}}</p>-->
                                    <!--<span>License:{{containerObj.license}}</span>-->
                                </div>
                            </div>
                      </div>
                       <Table :columns="resultsTableCol" :data="containerObj.images"></Table>
                 </Col>
                 <Col span="4">
                    <Card dis-hover class="card">
                       <p slot="title"><!-- <i class="fas fa-link icon-tag"></i> -->Similar Containers</p>
                       <div class="list-wrapper">
                            <!--<Card dis-hover class="similarity-card" v-for="item in similarProjects" :key="item.accession">-->
                              <!--<div class="similarity-title"><a @click="gotoDetails(item.name)">{{item.name}}</a></div>-->
                              <!--<div><span>{{item.title}}</span></div>-->
                            <!--</Card>-->
                           <Card v-for="item in similarProjects" class="card" v-bind:key="item.id">
                               <p slot="title"><a class="tool-name" @click="gotoDetails(item.id)">{{item.name}}</a></p>
                               <p slot="extra">
                                   <Tooltip>
                                       <Icon type="logo-codepen" size="22"/>
                                       <div class="tooltip-content" slot="content">
                                           {{item.description}}
                                       </div>
                                   </Tooltip>
                               </p>
                               <div class="card-content-wrapper">
                                   <div class="left">
                                       <div class="description-wrapper">
                                           <!--<Input v-model="item.description" disabled type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="" />-->
                                           <read-more more-str="" :text="item.title" link="#" less-str="read less" :max-chars="120"></read-more>
                                       </div>
                                       <!--<div class="state-wrapper">-->
                                           <!--{{item.state}}-->
                                       <!--</div>-->
                                   </div>

                               </div>
                           </Card>
                       </div>
                    </Card>
                 </Col>
            </Row>
          </div>
      </div>
  </div>
</template>

<script>


import store from "@/store/store.js"
import VulnerabilitiesModal from './VulnerabilitiesModal'
export default {
  name: 'tools',
  components: {
    VulnerabilitiesModal: VulnerabilitiesModal
  },
  data () {
    return {
        showModal: false,
        keywords:'',
        total:1000,
        current:1,
        pageSize:30,
        containerObj:{
            name:'',
            description:'',
            license:'',
            url:'',
            version:'',
            images:[]
        },
        loading:true,
        dataFound:false,
        filter:'All',
        resultsTableCol:[

            {
                title: 'Type',
                key: 'type',
                align: 'center',
                width: 65,
                render:(h,params) => {
                    return h('img', {
                        attrs: {
                            src: params.row.type,
                        },
                        style: {
                            display:'inline-block',
                            width: '100%'
                        },
                    })
                }
            },
            {
                title: 'Tool',
                key: 'tool',
                align: 'center',
                width: 120,

            },
            {
                title: 'Version',
                key: 'version',
                align: 'center',
                sortable: true,
                width: 100,
            },
            {
                title: 'Modified',
                key: 'last_updated',
                align: 'center',
                sortable: true,
                width: 105,
            },
            {
                title: 'Size',
                key: 'size',
                align: 'center',
                sortable: true,
                width: 85,
            },
            {
                title: 'Full Tag ',
                key: 'full_tag',
                // align: 'center',
                render: (h, params) => {
                            const row = params.row;
                            const color = 'blue';
                            const text = row.full_tag;

                            return h('div', {
                              style: {
                                  display:'flex',
                                      alignItems:'center'
                                  },
                              },[
                                  h('Tag', {
                                      props: {
                                         // type: 'box',
                                          color: color
                                      },
                                      style: {
                                          color: 'black',
                                          flex: '1'
                                      }
                                  },text),
                                  h('Icon', {
                                      on: {
                                          click: () => {
                                              this.doCopy(text)
                                          }
                                      },
                                      props: {
                                          type: 'ios-copy-outline',
                                          size: '14'
                                      },
                                      style: {
                                          marginLeft: '5px',
                                          display:'inline-block',
                                          cursor:'pointer'
                                      },
                                  }),
                              ]);

                }
            },
            {
                title: 'security',
                key: 'security',
                align: 'center',
                width: 85,
                render: (h, params) => {
                            const row = params.row;
                            const color = 'blue';

                            return h('div', {
                              style: {
                                  display:'flex',
                                      alignItems:'center'
                                  },
                              },[
                                  h('Icon', {
                                      on: {
                                          click: () => {
                                            this.getAnchoreImage(row)
                                          }
                                      },
                                      props: {
                                          type: 'ios-copy-outline',
                                          size: '14'
                                      },
                                      style: {
                                          marginLeft: '5px',
                                          display:'inline-block',
                                          cursor:'pointer'
                                      },
                                  }),
                              ]);

                }
            },
        ],
        licenseColor:{
          Apache: 'brightgreen',
          MIT:'green',
          GPL:'blue',
          BSD:'yellow',
          CC:'blueviolet',
          Artistic:'important'
        },
        similarProjects:[]
    }
  },
  methods:{
    rowClick(row){
      console.log('row',row);
        this.$router.push({name:'tools',params:{id:row.ID}});
    },
    filterClick(index){
        if(index == 0){
          for(let i in this.filters){
              if(i == index){
                this.filter = this.filters[i].name;
                this.filters[i].type = 'primary';
              }
              else
                this.filters[i].type = 'default';
          }
        }
        else{
            this.filters[0].type = 'default';
            if(this.filters[index].type == 'primary')
                this.filters[index].type = 'default';
            else{ 
                this.filter = this.filters[index].name;
                this.filters[index].type = 'primary';
            } 
        }
    },
    sortClick(index){
          for(let i in this.sorts){
              if(i == index)
                this.sorts[i].type = 'primary';
              else
                this.sorts[i].type = 'default';
          }
    },
    getAnchoreImage(container) {
        let ctx = this
        this.$http
            .get('https://jenkins.biocontainers.pro/security/v1/images', {params:{
              fulltag: "docker.io/" + container.full_version,
              history: false
            }})
            .then(function (res) {
              if (res.body && res.body.length > 0) {
                let digest = res.body[0].imageDigest
                ctx.getVulnerabilities(digest)
              }
            }).catch(function(err) {
              ctx.$modal.show('vulnerabilities', {vulnerabilities: [], msg: 'Not analysed yet'})
            })
    },
    getVulnerabilities(digest) {
      let ctx = this;
        this.$http
            .get('https://jenkins.biocontainers.pro/security/v1/images/' + digest + '/vuln/all')
            .then(function (res) {
              ctx.$modal.show('vulnerabilities', {vulnerabilities: res.body.vulnerabilities, msg: ''})
              
            }).catch(function(err) {

            })
    },
    toolInfo(id){
        console.log('this.$router.params.id',id)
        this.$http
            .get(this.$store.state.baseApiURL + '/api/ga4gh/v2/tools/'+ id)
            .then(function (res) {
                console.log('res.body', res.body);
                let resbody = res.body;
                this.containerObj.versions = []
                this.containerObj = {
                        name:resbody.toolname.toUpperCase(),
                        license:'',
                        description: resbody.description,
                        // url: resbody.url,
                        versions:[],
                        images:[]
                      };
                let found=false;
                for(let j in this.licenseColor){
                    if(resbody.license&&resbody.license.match(j)){
                      this.containerObj.license = 'https://img.shields.io/badge/license-'+encodeURIComponent(resbody.license).replace(/-/g,'--') + '-'+ this.licenseColor[j]+'.svg';
                      found=true;
                      break;
                    }
                }
                if(resbody.license&&!found){
                    this.containerObj.license = 'https://img.shields.io/badge/license-'+encodeURIComponent(resbody.license).replace(/-/g,'--') + '-lightgrey.svg';
                }
                for(let i = 0; i < resbody.versions; i++){
                    var version_item = {
                        tool: current_version.name,
                        version: current_version.meta_version
                    };
                    this.containerObj.versions.push(version_item);
                }
            })

    },
    containerID(id){
         this.$http
            .get(this.$store.state.baseApiURL + '/api/ga4gh/v2/tools/'+ id +'/versions')
            .then(function(res){
                console.log('res.body',res.body);
                let resbody=res.body[0];
                this.containerObj.images=[]
                let all_versions = res.body;
                for(let j = 0 ; j < all_versions.length; j++){
                    let current_version = all_versions[j];
                    for(let i=0; i < current_version.container_images.length; i++){
                        let original_type = "/static/logo/biocontainers-logo.png";
                        let prefix = '';
                        if(current_version.container_images[i].container_type === 'DOCKER'){
                            original_type = "/static/images/docker.png";
                            prefix = 'docker pull ';
                        }else if(current_version.container_images[i].container_type === 'CONDA'){
                            original_type = "/static/images/conda.png";
                            prefix = 'conda install -c conda-forge -c bioconda ';
                        }
                        var item = {
                            tool: current_version.name,
                            version: current_version.meta_version,
                            full_tag: prefix + current_version.container_images[i].full_tag,
                            size: (current_version.container_images[i].size/1048576).toFixed(2) + "M",
                            last_updated: current_version.container_images[i].hasOwnProperty('last_updated')? current_version.container_images[i].last_updated.substring(0,10): '',
                            type: original_type,
                            full_version: current_version.container_images[i].full_tag
                        };
                        this.containerObj.images.push(item);
                    }
                }
            },function(err){
                console.log('err',err);
                this.dataFound=false;
                this.loading=false;
                this.$Notice.error({
                    title: 'Server Error',
                    desc: err.body.error
                });
            });
    },
    containerVersion(){

    },
    doCopy(value) {
      if (value) {
        try {
          console.log('copy value',value)
          const input = document.createElement('input');
          document.body.appendChild(input);
          input.setAttribute('value', value);
          input.select();
          document.execCommand('copy');
          this.$Message.success({ content: 'Copy Successfully', duration: 1 });
          document.body.removeChild(input);
        } catch (e) {
          this.$Message.error({ content: 'Copy Failed', duration: 1 });
          document.body.removeChild(input);
        }
      } else
        this.$Message.error({ content: 'No value to Copy', duration: 1 });
    },

    gotoDetails(id){
      //this.$router.push({name:'dataset',params:{id:id}});
      this.$router.push({name:'tools',params:{id:id}});
      
    },
    getSimilars(id){
        this.$http
            .get(this.$store.state.baseApiURL + '/api/ga4gh/v2/tools/'+ id + '/similars')
            .then(function (res) {
                // console.log('res.body similars', res.body);
                this.similarProjects = []
                let resbody = res.body;
                resbody = resbody.sort((a, b) => (a.similar_score < b.similar_score) ? 1 : -1)
                for(let i = 0; i < resbody.length; i++){
                    var tool = {
                        name: resbody[i].toolname,
                        title: resbody[i].description,
                        id: resbody[i].id
                    };
                    this.similarProjects.push(tool);
                }
            })

    },
  },
  beforeRouteUpdate (to, from, next) {
    //console.log('from',from)
     this.toolInfo(to.params.id);
     this.containerID(to.params.id);
     this.getSimilars(this.$route.params.id);
     this.containerVersion();
     next();
  },
  mounted(){
    this.toolInfo(this.$route.params.id);
    this.containerID(this.$route.params.id);
    this.containerVersion();
    this.getSimilars(this.$route.params.id);
  }
}


</script>




<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .search-wrapper{
      width: 100%;
      text-align: center;
      margin: 50px auto 0 auto;
    }
    .search-options-wrapper{
      margin: 20px auto 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .filter-wrapper{
      display: flex;
    }
    .filter-wrapper .sort{
      margin-left: 10px;
    }
    .filter-wrapper .name{
      font-size: 0.875rem
    }
    .results-wrapper{
      width: 80%;
      margin: 30px auto 0 auto;
    }
    .update-statistics{
      width: 80%;
      margin: 30px auto 0 auto;
    }
    .issue-statistics{
      width: 80%;
      margin: 30px auto 0 auto;
    }
    .banner{
      background-color: #eb8c1f;
      color: #ffffff;
      padding: 3rem 0;
    }
    .triangle-down:before{
     
      /*background-image:url('static/triangle.svg');*/
    }
    .triangle:before{
      background-repeat: no-repeat;
      background-size: 100% 100%;
      content: '';
      display: block;
      width: 100%;
      left: 0;
      height: 30px;
      /*background-image:url('static/triangle.svg');*/
    }
    .spin-container{
      display: inline-block;
      width: 100%;
      height: 100px;
      position: relative;
    }
    .no-data-container{
      width: 100%;
      text-align: center;
      font-size: 14px;
    }
    .title-container{
        width: 100%;
        margin: 0 auto 10px auto;
        display: flex;
        justify-content: space-between;
    }
    .title-wrapper{
        border: 1px solid #eee;
        border-left-width: 4px;
        border-radius: 4px;
        margin-bottom: 4px;
        padding: 7px 15px;
        display: inline-block;
        width: 100%;
    }
    .card-title{
      text-align: left !important;
      overflow: auto;
      font-size: 14px;
    }

    .card-title .block{
      text-align: left !important;
      margin:10px;
      overflow: auto;
      position: relative;
    }

    .content-wrapper{
      width: 80%;
        padding-top: 35px;
      padding-right: 15px;
      padding-left: 15px;
      margin-right: auto;
      margin-left: auto;
      -ms-flex-wrap: wrap;
      flex-wrap: wrap;
      -ms-flex-wrap: wrap;
    }
    .title{
      font-size: 4.5rem;
      font-weight: 300;
      line-height: 1.2;
    }
    .description{
      font-size: 1.25rem;
      font-weight: 300;
    }
    .content{
      position: relative;
      min-height: 300px;
      margin-bottom: 6rem;
      font-size: 1.1rem;
      line-height: 1.6;
      width: 80%;
      margin-right: auto;
      margin-left: auto;

    }
    .card-content-wrapper{
      display: flex;
      justify-content: space-between;
    }
    .card-content-wrapper .right{
      display: flex;
      align-items: end;
      font-size: 30px;
    }
    .content h1{
      border-bottom: 1px solid #e4973e;
      font-weight: 500;
      padding-top: 60px;
      color: #eb8c1f;
    }
    .container-wrapper{
      margin-top: 50px;
      padding-top: 15px;
    }
    .description-wrapper{
      margin-bottom: 5px;
      white-space: normal;
    }
    .tag-wrapper{
      margin-bottom: 5px;
      display: inline-block;
    }
    .card{
      width: 100%;
      margin-bottom: 30px;
      min-height: 100px;
      overflow: hidden;
      transition: all 0.15s ease-out;
      -webkit-transition: all 0.15s ease-out;
    }
    .tooltip-content{
        white-space: normal;
        width: 200px;
    }
    .page-wrapper{
      text-align: center;
      font-size: 12px;
    }
    .filter-button{
      min-width: 70px;
    }
    .license-wrapper{
      display: flex;
      align-items: center;
    }
    .license-img{
      margin-left: 10px;
    }
    .similarity-card{
      margin-bottom: 5px;
    }
    .card a{
        color: #495060;
    }
    .card a:hover{
          color: #eb8c1f;
    }
</style>

<style>
    .update-statistics .ivu-card-head{
      background-color: #d9edf7 !important;
    }
    .update-statistics .ivu-card-bordered{
      border: 1px solid #bce8f1 !important;
      border-color: #bce8f1 !important;
    }
    .issue-statistics .ivu-card-head{
      background-color: #dff0d8 !important;
    }
    .issue-statistics .ivu-card-bordered{
      border: 1px solid #d6e9c6 !important;
      border-color: #d6e9c6 !important;
    }

</style>
