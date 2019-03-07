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
          <!--<h1>Search</h1>-->
          <!--<div class="search-wrapper">-->
            <!--<Input v-model="keywords" icon="ios-search" placeholder="Search" style="width:100%"></Input>-->
          <!--</div>-->
          <!--<div class="search-options-wrapper">-->
              <!--<div class="filter-wrapper">-->
                  <!--<div class="filter">-->
                        <!--<span class="name">Filters:</span>-->
                        <!--<ButtonGroup>-->
                            <!--<Button class="filter-button" v-for="(item ,index) in filters" :type="item.type" :key="index" @click="filterClick(index)">{{item.name}}</Button>-->
                        <!--</ButtonGroup>-->
                  <!--</div>-->
              <!--</div>-->
              <!--&lt;!&ndash;<div class="search-button-wrapper">&ndash;&gt;-->
                  <!--&lt;!&ndash;<Button type="primary" @click="search">Search</Button>&ndash;&gt;-->
              <!--&lt;!&ndash;</div>&ndash;&gt;-->
          <!--</div>-->
          <div class="container-wrapper">
            <div class="title-container">
                  <div class="title-wrapper">
                      <div class="card-title">
                        <span>Tool: {{containerObj.name}}</span>
                        <!--<span>License:{{containerObj.license}}</span>-->
                      </div>
                  </div>
                  <!--
                  <div class="title-wrapper">
                      <div class="card-title">
                        <span>Images</span>
                      </div>
                  </div>
                  -->
            </div>
            <!--<div class="container-wrapper-cards">-->
                <!--<Card v-for="item in containerObj.versions" class="card">-->
                      <!--<p slot="title">{{item.tool}}</p>-->
                      <!--<p slot="extra">{{item.version}}</p>-->
                      <!--<div class="card-content-wrapper">-->
                        <!--<div class="left">-->
                            <!--<div class="description-wrapper">-->
                              <!--<read-more more-str="" :text="item.description" link="#" less-str="read less" :max-chars="120">-->

                              <!--</read-more>-->
                              <!--<img class="license-img" :src="item.license"/>-->
                            <!--</div>-->
                            <!--<div class="state-wrapper">-->
                                <!--{{item.state}}-->
                            <!--</div>-->
                        <!--</div>-->
                      <!--</div>-->
                  <!--</Card>-->
              <!--</div>-->


            <!--<div class="card-content-wrapper">-->
                      <!--<Card dis-hover v-for="item in containerObj.images" class="card">-->
                            <!--<p slot="title">Container Images</p>-->
                            <!--<div>-->
                                <!--<span>Tag: </span><span>{{item.fullTag}}</span>-->
                            <!--</div>-->

                            <!--<div>-->
                                <!--<span>Size: </span><span>{{item.size}}M</span>-->
                            <!--</div>-->
                            <!--<div>-->
                                <!--<span>Last Update: </span><span>{{item.last_update}}</span>-->
                            <!--</div>-->
                      <!--</Card>-->
                  <!--</div>-->
           <Table :columns="resultsTableCol" :data="containerObj.images"></Table>
          </div>
          
      </div>
      <!--
      <div class="results-wrapper">
          <Table stripe :columns="resultsTableCol" :data="resutls" @on-row-click="rowClick"></Table>
      </div>
      <div class="update-statistics">
          <Card style="width:100%" class="">
              <p slot="title">Containers Update Statistics</p>
          </Card>
          <Card style="width:100%" class="">
              <p slot="title">Containers Update Statistics</p>
          </Card>
      </div>
      -->
      <!--
      <div class="issue-statistics">
          <Card style="width:100%" class="issue-statistics-card">
              <p slot="title">GitHub Issues Statistics </p>
          </Card>
      </div>
      -->
  </div>
</template>

<script>
import store from "@/store/store.js"
export default {
  name: 'tools',
  data () {
    return {
        keywords:'',
        total:1000,
        current:1,
        pageSize:30,
        containerObj:{
            name:'',
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
                render:(h,params) => {
                    return h('img', {
                        attrs: {
                            src: params.row.type,
                        },
                        style: {
                            display:'inline-block',
                            width: '30%'
                        },
                    })
                }
            },
            {
                title: 'Tool',
                key: 'tool',
                align: 'center',
            },
            {
                title: 'Version',
                key: 'version',
                align: 'center',
                sortable: true
            },
            {
                title: 'Modified',
                key: 'last_updated',
                align: 'center',
                sortable: true
            },
            {
                title: 'Size',
                key: 'size',
                align: 'center',
                sortable: true
            },
            {
                title: 'Full Tag ',
                key: 'full_tag',
                width:400,
                // align: 'center',
                render: (h, params) => {
                            const row = params.row;
                            const color = 'blue';
                            const text = row.full_tag;

                            return h('Tag', {
                                props: {
                                    type: 'box',
                                    color: color
                                },
                                style: {
                                    color: 'black'
                                }
                            }, text);
                        }
            },



        ],
        resutls:[
            {
                container: 'John Brown',
                description: 18,
                realname: 'New York No. 1 Lake Park',
                lastmodified: '2016-10-03',
                starredstarts:'test',
                popularity:'test',
                registrylink:'test'
            },
            {
                container: 'John Brown',
                description: 18,
                realname: 'New York No. 1 Lake Park',
                lastmodified: '2016-10-03',
                starredstarts:'test',
                popularity:'test',
                registrylink:'test'
            },
            {
                container: 'John Brown',
                description: 18,
                realname: 'New York No. 1 Lake Park',
                lastmodified: '2016-10-03',
                starredstarts:'test',
                popularity:'test',
                registrylink:'test'
            },
            {
                container: 'John Brown',
                description: 18,
                realname: 'New York No. 1 Lake Park',
                lastmodified: '2016-10-03',
                starredstarts:'test',
                popularity:'test',
                registrylink:'test'
            },
        ],
        filters:[
            {
                name:'All',
                type:'primary',
            },
            {
                name:'ID',
                type:'default',
            },
            {
                name:'Name',
                type:'default',
            },
            {
                name:'Description',
                type:'default',
            },
        ],
        sorts:[
            {
                name:'sort1',
                type:'primary',
            },
            {
                name:'sort2',
                type:'default',
            },
            {
                name:'sort3',
                type:'default',
            }
        ],
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
    containerID(){
            console.log('this.$router.params.id',this.$route.params.id);
         this.$http
            .get(this.$store.state.baseApiURL + '/api/ga4gh/v2/tools/'+ this.$route.params.id+'/versions')
            .then(function(res){
                      console.log('res.body',res.body);
                      let resbody=res.body[0];
                      this.containerObj = {
                        name:resbody.name.toUpperCase(),
                        version:resbody.meta_version,
                        license:resbody.license,
                        versions:[],
                        images:[]
                      };

                      let all_versions = res.body;
                      for(let j = 0 ; j < all_versions.length; j++){
                          let current_version = all_versions[j];
                          var version_item = {
                              tool: current_version.name,
                              version: current_version.meta_version
                          };
                          this.containerObj.versions.push(version_item);

                          for(let i=0; i < current_version.container_images.length; i++){
                              let original_type = "/static/logo/biocontainers-logo.png";
                              let prefix = '';
                              if(current_version.container_images[i].container_type === 'DOCKER'){
                                  original_type = "/static/images/docker.png";
                                  prefix = 'docker pull ';
                              }else if(current_version.container_images[i].container_type === 'CONDA'){
                                  original_type = "/static/images/conda.png";
                                  prefix = 'conda install ';
                              }
                              var item = {
                                  tool: current_version.name,
                                  version: current_version.meta_version,
                                  full_tag: prefix + current_version.container_images[i].full_tag,
                                  size: (current_version.container_images[i].size/1024).toFixed(2) + "M",
                                  last_updated: current_version.container_images[i].hasOwnProperty('last_updated')? current_version.container_images[i].last_updated.substring(0,9): '',
                                  type: original_type
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

    }
  },
  mounted(){
    this.containerID();
    this.containerVersion();
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
        margin:0 5px;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
    }
    .content-wrapper{
      width: 80%;
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
    /*
    @media (max-width: 840px) { 
      .card{ 
        width: calc((100% - 0px) / 1 - 3px);
       
      }
    }
    @media (max-width: 1015px) and (min-width: 841px){ 
      .card{ 
        width: calc((100% - 60px) / 2 - 3px);

      }
      .container-wrapper{
       
      }
    }
    @media (max-width: 1510px) and (min-width: 1016px){ 
      .card{ 
        width: calc((100% - 90px) / 3 - 4px);
      }
      .container-wrapper{
        
      }
    }
    @media (max-width: 3910px) and (min-width: 1511px){ 
      .card{ 
        width: calc((100% - 120px) / 4 - 4px);
      }
      .container-wrapper{
        
      }
    }*/
   
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
    /*
    table tr:last-child td:first-child {
        border-bottom-left-radius: 10px;
    }

    table tr:last-child td:last-child {
        border-bottom-right-radius: 10px;
    }
    */
</style>
