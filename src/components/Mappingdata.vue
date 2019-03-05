<template>
  <div class="index-container">
      <div class="banner">
          <div class="content-wrapper">
              <h1 class="title">BioContainers</h1>
              <p class="description">Statistics, GitHub Issues, and BioCotnainers usage</p> 
          </div>
      </div>
      <div class="triangle triangle-down"></div>
      <div class="content">
         <Card class="card">
              <p slot="title">GitHub Issues Statistics</p>
              <Heatmap></Heatmap>
        </Card>
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
import Heatmap from '@/components/charts/Heatmap.vue'
const moment = require('moment');
export default {
  name: 'MappingData',
  data () {
    return {
        QUAY_ORGANIZATION:"https://quay.io/api/v1/repository?namespace=biocontainers&popularity=true&last_modified=true",
        RetrieveGitHubIssuesAPI1:"https://api.github.com/repos/biocontainers/containers/issues?state=all&per_page=100",
        RetrieveGitHubIssuesAPI2:"https://api.github.com/repos/biocontainers/specs/issues?state=all&per_page=100",
        RetrieveGitHubIssuesAPI3:"https://api.github.com/repos/biocontainers/specs/issues/comments?per_page=100",
        RetrieveGitHubIssuesAPI4:"https://api.github.com/repos/biocontainers/containers/issues/comments?per_page=100",
        dates:{},
        githubdates:[],
        githubDatesMap:{},
        keywords:'',
        resultsTableCol:[
            {
                title: 'Container',
                key: 'container'
            },
            {
                title: 'Description',
                key: 'description'
            },
            {
                title: 'Real Name',
                key: 'realname'
            },
            {
                title: 'Last Modified',
                key: 'lastmodified'
            },
            {
                title: 'Starred/Starts',
                key: 'starredstarts'
            },
            {
                title: 'Popularity',
                key: 'popularity'
            },
            {
                title: 'Registry Link',
                key: 'registrylink'
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
                name:'Cancel',
                type:'default',
            },
            {
                name:'Confirm',
                type:'default',
            },
            {
                name:'Confirm',
                type:'default',
            },
            {
                name:'Confirm',
                type:'default',
            }
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
  components: {
      Heatmap,
  },
  methods:{
    test(){
      this.$http
            .get('/api/get')
            .then(function(res){
              console.log(res);
                console.log(123);
            },function(err){

            });
    },
    retrieveGitHubIssues(){
       
      let promise1 = this.$http.get(this.RetrieveGitHubIssuesAPI1);
      let promise2 = this.$http.get(this.RetrieveGitHubIssuesAPI2)
      let promise3 = this.$http.get(this.RetrieveGitHubIssuesAPI3)
      let promise4 = this.$http.get(this.RetrieveGitHubIssuesAPI4)
           
      Promise.all([promise1, promise2, promise3, promise4]).then(([v1,v2,v3,v4]) => {
        //console.log('v1',v1.data);
        let data1 = v1.data;
        let data2 = v2.data;
        let data3 = v3.data;
        let data4 = v4.data;
        console.log('v1.data',v1.data)
        for(let i in data1){
            //let createAt   = new Date(data1[i].created_at).toLocaleDateString();
            let createAt   = moment(data1[i].created_at).format('DD/MM/YYYY')
            let modifiedAt = new Date(data1[i].updated_at).toLocaleDateString();
            let closeAt    = new Date(data1[i].close_at).toLocaleDateString();
            this.githubdates.push(createAt);
            //this.githubdates.push(modifiedAt);
            //this.githubdates.push(closeAt);
        }
        /*
        for(let i in data2){
            let createAt   = new Date(data2[i].created_at).toLocaleDateString();
            let modifiedAt = new Date(data2[i].updated_at).toLocaleDateString();
            let closeAt    = new Date(data2[i].close_at).toLocaleDateString();
            this.githubdates.push(createAt);
            this.githubdates.push(modifiedAt);
            this.githubdates.push(closeAt);
        }

        for(let i in data3){
            let createAt   = new Date(data3[i].created_at).toLocaleDateString();
            let modifiedAt = new Date(data3[i].updated_at).toLocaleDateString();
            let closeAt    = new Date(data3[i].close_at).toLocaleDateString();
            this.githubdates.push(createAt);
            this.githubdates.push(modifiedAt);
            this.githubdates.push(closeAt);
        }

        for(let i in data4){
            let createAt   = new Date(data4[i].created_at).toLocaleDateString();
            let modifiedAt = new Date(data4[i].updated_at).toLocaleDateString();
            let closeAt    = new Date(data4[i].close_at).toLocaleDateString();
            this.githubdates.push(createAt);
            this.githubdates.push(modifiedAt);
            this.githubdates.push(closeAt);
        }
       */

       //this.githubdates = ['19/10/2018','18/10/2018','18/10/2018','18/10/2018','18/10/2018','17/10/2018','16/10/2018','03/10/2018']
      
        for(let i in this.githubdates){
            this.githubDatesMap[this.githubdates[i]] = this.githubDatesMap[this.githubdates[i]] ? this.githubDatesMap[this.githubdates[i]]+1 : 1;
        }
        console.log('this.githubDatesMap',this.githubDatesMap)

        this.$bus.$emit('show-issue', this.githubDatesMap);


/*
       this.githubdates = ['19/10/2018','18/10/2018','18/10/2018','18/10/2018','18/10/2018','17/10/2018','16/10/2018','03/10/2018']
      
        for(let i in this.githubdates){


          console.log('11',this.githubdates[i]);
            var parts = this.githubdates[i].split('/');
            var dateNumber = new Date(parts[2]+"-"+parts[1]+"-"+parts[0]).getTime()/1000;
            var num = Math.floor(dateNumber);
            if(!isNaN(num)) {
                this.githubDatesMap[num.toString()] = this.githubDatesMap[num.toString()] ? this.githubDatesMap[num.toString()]+1 : 1;
            }
        }
      console.log('this.githubDatesMap',this.githubDatesMap);
        let tempArray = [];
        for(let i in this.githubdates){
          let date = new Date(parseFloat(i));
          let item = {
            time:moment(date).format('DD-MM-YYYY'),
            value:this.githubDatesMap[i]
          }
          tempArray.push(item);
        }

        console.log('tempArray',tempArray);
        console.log('optimizeArray',this.optimizeArray(tempArray));
        this.$bus.$emit('show-issue', tempArray);*/
      })
    },
    retrieveQuayIO(){
      this.$http
            .get(this.QUAY_ORGANIZATION,{headers: {'X-Requested-With' :'XMLHttpRequest','Authorization': "Bearer "+ "XRYLsxvQqmQLpP7RrajpFdiZntveNEyiffXyibK0"}})
            .then(function(res){
              //console.log('retrieveQuayIO',res);
              let repositories = res.body.repositories
                for(let i in repositories){
                   let item = {
                      domain: "quay.io/biocontainers/",
                      name: repositories[i].name, 
                      description: repositories[i].description, 
                      lastModified: repositories[i].last_modified, 
                      number_pull: [repositories[i].popularity, 50], 
                      start_count:repositories[i].is_starred
                   }

                   let num = Math.floor(repositories[i].last_modified/1000)
                   if(!isNaN(num))
                      this.dates[num.toString()] = this.dates[num.toString()] ? this.dates[num.toString()]+1:1;
                }

              

                //console.log('this.dates',this.dates);
            },function(err){
              console.log('err',err);
            });
    },
    search(){
        console.log('search');
        
    },
    optimizeArray(array){
        let value;
        let tempArray = [];
        for(let i =0;i<array.length-1; i++){
            //console.log(array[i].time);
            //console.log(array[i+1].time);
          if(array[i].time == array[i+1].time){
            //console.log('true');
            value = array[i].value + array[i+1].value;
          }
          else{
            console.log('push');
            let item = {
              time: array[i].time,
              value: value,
            }
            tempArray.push(item);
          }
        }
        return tempArray;
    }
  },
  mounted(){

    this.retrieveQuayIO();
    this.retrieveGitHubIssues();
    //this.test();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    
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
      min-height: 300px;
      margin-bottom: 6rem;
      font-size: 1.1rem;
      line-height: 1.6;
      width: 80%;
      margin-right: auto;
      margin-left: auto;
    }
    .content h1{
      border-bottom: 1px solid #e4973e;
      font-weight: 500;
      padding-top: 60px;
      color: #eb8c1f;
    }
</style>


