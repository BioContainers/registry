<template>
  <div class="multipackage-container">
      <div class="banner">
          <div class="content-wrapper">
              <h1 class="title">Multi-package Containers</h1>
              <p class="description">Combine several conda packages into one Docker container</p> 
          </div>
      </div>
      <div class="content-container">
          <div class="packages-wrapper">
              <Card class="card">
                  <p slot="title">Packages</p>
                  <div class="search-wrapper">
                    <Input v-model="keywords" icon="ios-search" placeholder="Search" style="width:100%" @on-change="search"></Input>
                  </div>
                  <Table stripe :columns="resultsTableCol" :data="resutls" :loading="loading"></Table>
                  <div class="page-wrapper">
                    <!--
                      <Page :total="total" :current="current" :page-size="pageSize" size="small" show-elevator show-sizer @on-change="pageChange" @on-page-size-change="pageSizeChange"/>
                    -->
                      <Page :total="total" :current="current" :page-size="pageSize" size="small"  @on-change="pageChange"/>
                  </div>
              </Card>
          </div>
          <div v-if="selectedPackagesResutls.length>0" class="packages-wrapper selected-packages">
              <Card class="card">
                  <p slot="title">Selected Packages</p>
                  <Alert v-if="containerRepeated" type="error">{{containerRepaetedName}} Container Repeated</Alert>
                  <Table stripe :columns="selectedPackagesTableCol" :data="selectedPackagesResutls"></Table>
                  <div class="button-wrapper">
                      <Button type="error" @click="selectedPackagesClear">Clear</Button>
                  </div>
                  <div class="details-wrapper">
                      <p>To create a container, please add the following string to this file as a pull request:</p>
                      <div class="textarea-wrapper"> 
                        <Input v-model="createContainerValue" disabled type="textarea" placeholder="Enter something..." />
                      </div>
                      <p>Container name:</p>
                      <div class="textarea-wrapper"> 
                        <Input v-model="containerNameValue" disabled type="textarea" placeholder="Enter something..." />
                      </div>
                  </div>
                  <div class="button-wrapper">
                      <!--<a class="download-button" :href="downloadHref" :download="downloadName">-->
                      <Button type="success" @click="download">Download</Button>
                  </div>
              </Card>
          </div>
     
      </div>
      <!--<iframe class="lorikeet-iframe" src="http://biocontainers.pro/multi-package-containers/" scrolling="no"></iframe>-->
  </div>

</template>

<script>
import { each, union } from 'lodash';
import { createHash } from 'crypto';


export default {
  name: 'ContainerDetails',
  
  data () {
    return {
        keywords:'',
        total:0,
        current:1,
        pageSize:10, 
        loading:true,
        packages:[],
        content:'',
        containerName:'',
        containerRepeated:false,
        containerRepaetedName:'',
        //downloadHref:'',
        //downloadName:'',
        createContainerValue: '2pg_cartesian=1.0.1,_license=1.1,_nb_ext_conf=0.3.0,abawaca=1.00,abricate=0.4,abstract-rendering=0.5.1,abundancebin=1.0.1',
        containerNameValue:'quay.io/biocontainers/mulled-v2-87f6cdd7eada4e4f6f2fc092e7820d826d5aeeaa:5b8a8a59d2a5385e45cbe82909bf44e7544071f1',
        dataApi1: 'static/repodata/anaconda/repodata.json', 
        dataApi2: 'static/repodata/bioconda/repodata.json',
        dataApi3: 'static/repodata/conda-forge/repodata.json', 
        resultsTableCol:[
            {
                title: 'Name',
                key: 'name'
            },
            {
                title: 'Version',
                key: 'version'
            },
            {
                title: 'Channel',
                key: 'channel'
            },
            {
                title: '',
                key: 'action',
                align:'center',
                width:100,
                render: (h, params) => {
                    return h('div', [
                        /*
                        h('Button', {
                           
                            on: {
                                click: () => {
                                    this.gotoBlast(params);
                                }
                            }
                        }, 'Blast'),
                        */
                        h('Icon', {
                            props: {
                                type: 'md-add',
                            },
                            style: {
                                marginLeft: '5px'
                            },
                            on: {
                                click: () => {
                                    this.selectedPackagesRowAdd(params.row);
                                }
                            }
                        }),
                    ]);
                }
            }
        ],
        resutls:[],
        selectedPackagesTableCol:[
            {
                title: 'Name',
                key: 'name'
            },
            {
                title: 'Version',
                key: 'version'
            },
            {
                title: '',
                key: 'action',
                align:'center',
                width:100,
                render: (h, params) => {
                    return h('div', [
                        /*
                        h('Button', {
                           
                            on: {
                                click: () => {
                                    this.gotoBlast(params);
                                }
                            }
                        }, 'Blast'),
                        */
                        h('Icon', {
                            props: {
                                type: 'md-remove',
                            },
                            style: {
                                marginLeft: '5px'
                            },
                            on: {
                                click: () => {
                                    this.selectedPackagesRowRemove(params.row);
                                }
                            }
                        }),
                    ]);
                }
            }
        ],
        selectedPackagesResutls:[],
    }
  },
  methods:{
    selectedPackagesRowAdd(rowItem){
        var found = false;
        for(let i in this.selectedPackagesResutls){
          if(this.selectedPackagesResutls[i]&&this.selectedPackagesResutls[i].name.match(rowItem.name)){
              found=true;
              this.containerRepaetedName=rowItem.name;
              break;
          }
        }
        if(!found){
            var item={
                name:rowItem.name,
                version:rowItem.version
            }
            this.selectedPackagesResutls.push(item);
            this.createContainerValue = this.getContent();
            this.containerNameValue = this.getContainerName();
            //this.download();
        }
        else{
          this.containerRepeated=true;
          setTimeout(()=>{
            this.containerRepeated=false;
            this.containerRepaetedName='';
          },1500)
        }
    },
    selectedPackagesRowRemove(rowItem){
      this.selectedPackagesResutls.splice(rowItem._index, 1);
      if(this.selectedPackagesResutls.length>0){
          this.createContainerValue = this.getContent();
          this.containerNameValue = this.getContainerName();
          //this.download();
      }
    },
    selectedPackagesClear(){
      this.selectedPackagesResutls=[];
    },
    test(){
      /*
      Q.all([this.$http
            .get(this.dataApi),
            this.$http
            .get(this.dataApi),
            this.$http
            .get(this.dataApi)]).spread(function(){

      })*/
      Promise.all([
          this.$http.get(this.dataApi1),
          this.$http.get(this.dataApi2),
          this.$http.get(this.dataApi3),
      ]).then((data)=> {
            let anaconda = this.processData(data[0].body, 'anaconda');
            let bioconda = this.processData(data[1].body, 'bioconda');
            let condaforge = this.processData(data[2].body, 'conda-forge');
            let packages = union(anaconda, bioconda, condaforge);

            this.packages = packages.sort((a,b)=>{
              return a.name.localeCompare(b.name);
            });
            console.log(packages);
            this.loading=false;
            this.total = this.packages.length;
            this.resutls = packages.slice(0,this.pageSize);
      });
    },
    pageChange(page){
        page = page - 1;
        this.resutls=[];
        let start = page * this.pageSize;
        let end = start + this.pageSize;
        this.resutls = this.packages.slice(start,end);
    },
    pageSizeChange(pageSize){
      this.resutls=[];
      console.log('pageSizeChange',pageSize);
      console.log('this.current',this.current);
      let start = 0;
      let end = pageSize;
      console.log('start',start);
      console.log('end',end);
      this.resutls = this.packages.slice(start,end);
      console.log('this.resutls',this.resutls);
    },
    processData(data, channel) {
        let packages = [];
        let index = {};
        each(data.packages, (obj) => {
            const name = obj.name;
            const version = obj.version;
            const packageObject = {
                name: name,
                version: version,
                channel: channel
            };

            if (Object.keys(index).indexOf(name) === -1) {
                index[name] = version;
                packages.push(packageObject);
            } else {
                const idx = packages.findIndex((item) => {
                    return item.name === name;
                });

                // Always keep the freshest package
                if (packages[idx].version < version) {
                    index[name] = version;
                    packages[idx] = packageObject;
                }
            }
        });

        return packages;
    },
    getContent() {
        return this.selectedPackagesResutls.map((item) => {
            return item.name + '=' + item.version;
        }).join();
    },
    getContainerName() {
        let text = '';
        if (this.selectedPackagesResutls.length === 1) {
            const target = this.selectedPackagesResutls[0];
            text = target.name+':'+target.version;
        } else {
            const packageNames = this.selectedPackagesResutls.map((item) => item.name);
            const packageNamesString = packageNames.join('\n');
            let packageHash = createHash('sha1');
            packageHash.update(packageNamesString);
            packageHash = packageHash.digest('hex');

            const packageVersions = this.selectedPackagesResutls.map((item) => item.version || 'null');
            let versionHash;

            if (packageVersions.length > 0) {
                const packageVerisonsString = packageVersions.join('\n');
                versionHash = createHash('sha1');
                versionHash.update(packageVerisonsString);
                versionHash = versionHash.digest('hex');
            } else {
                versionHash = '';
            }

            text = 'quay.io/biocontainers/mulled-v2-'+packageHash+':'+versionHash;
        }

        return text;
    },
    download() {
        let content = this.createContainerValue;
        let filename = this.containerNameValue + '.tsv';
        let url = 'data:text/plain;charset=utf-8,' + encodeURIComponent(content);
        let elem = document.createElement('a');
        elem.setAttribute('href', url);
        elem.setAttribute('download', filename);
        document.body.appendChild(elem);
        elem.click();
        elem.remove();
    },
    search(){
      console.log('search',this.keywords);
      if(this.keywords==''){
        this.resutls = this.packages.slice(0,this.pageSize);
        this.total = this.packages.length;
        return;
      }
      if(this.packages.length>0){
          var temp=[];
          this.resutls = [];
          console.time('aaa');
          for(let i=0; i<this.packages.length;i++){
              if(this.packages[i].name.match(this.keywords) || this.packages[i].version.match(this.keywords) || this.packages[i].channel.match(this.keywords))
                temp.push(this.packages[i])
          }
          this.total=temp.length;
          this.resutls = temp.slice(0,this.pageSize);
      }
    }
  },
  mounted(){
      setTimeout(() => {
          this.test();
      }, 750);
    //console.log('receive id',this.$route.params.id);
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

    .multipackage-container{
         width: 100%;
         height: 100%;

    }
    .lorikeet-iframe{
        width: 100%;
        height: 100%;
        border-width:0;
    }
    .banner{
      background-color: #eb8c1f;
      color: #ffffff;
      padding: 3rem 0;
    }
    .search-wrapper{
      width: 100%;
      text-align: center;
      margin: 0 auto 10px auto;
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
    .content-container{
      width: 90%;
      text-align: center;
      margin: 30px auto;
      display: flex;
    }
    .selected-packages{
      margin-left: 10px !important;
    }
    .packages-wrapper{
      width: 50%;
      margin: 0 auto;
      display: inline-block;
    }
    .title{
      font-size: 4.5rem;
      font-weight: 300;
      line-height: 1.2;
    }
    .page-wrapper{
      margin-top: 10px;
      /*padding: 0 30px;*/
    }
    .card p{
      text-align: left;
    }
    .button-wrapper{
      margin:20px auto;
    }
    .textarea-wrapper{
      margin: 5px 0;
      white-space: nowrap;
    }
</style>

