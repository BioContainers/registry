<template>
  <div class="index-container">
      <!--<div class="banner">-->
          <!--<div class="content-wrapper">-->
              <!--<h1 class="title">BioContainers</h1>-->
              <!--<p class="description">Bioinformatics more accessible and reproducible</p>-->
          <!--</div>-->
      <!--</div>-->
      <div class="content">
          <h1>Search</h1>
          <div class="search-wrapper">
            <Input v-model="keywords" icon="ios-search" placeholder="Search" style="width:100%"></Input>
          </div>
          <div class="search-options-wrapper">
              <div class="filter-wrapper">
                  <div class="filter">
                        <span class="name">Filters:</span>
                        <ButtonGroup>
                            <Button class="filter-button" v-for="(item ,index) in filters" :type="item.type" :key="index" @click="filterClick(index)">{{item.name}}</Button>
                        </ButtonGroup>
                  </div>
              </div>
              <div class="search-button-wrapper">
                  <Button type="primary" @click="search">Search</Button>
              </div>
          </div>
          <div class="container-wrapper">

                  <Spin fix v-if="loading"></Spin>


                  <Card v-if="dataFound" v-for="item in cardList" class="card">
                      <p slot="title"><a class="tool-name" @click="gotoContainerDetails(item.id)">{{item.toolname}}</a></p>
                      <p slot="extra">
                        <Tooltip>
                            <Icon type="logo-codepen" size="22"/>
                            <div class="tooltip-content" slot="content">
                                {{item.content}}
                            </div>
                        </Tooltip>
                      </p>
                      <div class="card-content-wrapper">
                        <div class="left">
                            <div class="description-wrapper">
                              <!--<Input v-model="item.description" disabled type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="" />-->
                              <read-more more-str="" :text="item.description" link="#" less-str="read less" :max-chars="120"></read-more>
                              <img class="license-img" :src="item.license"/>
                            </div>
                            <div class="state-wrapper">
                                {{item.state}}
                            </div>
                        </div>
                        <div class="right">
                        </div>
                      </div>
                  </Card>
                  <div v-if="!dataFound" class="no-data-container">
                      No Data...
                  </div>


          </div>
          <div class="page-wrapper">
              <Page :total="total" :current="current" :page-size="pageSize" size="small" show-elevator show-sizer @on-change="pageChange" @on-page-size-change="pageSizeChange"/>
          </div>
      </div>
  </div>
</template>

<script>
const fixedEncodeURIComponent = (str) => {
return encodeURIComponent(str).replace(/[!'()*]/g, (c) => {

})
};
import store from "@/store/store.js"
export default {
  name: 'Registry',
  data () {
    return {
        keywords:'',
        total:1000,
        current:1,
        pageSize:30,
        cardList:[],
        loading:true,
        dataFound:false,
        filter:'All',
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
        query:{
          offset:1,
          limit:30
        },
        licenseColor:{
          Apache: 'brightgreen',
          MIT:'green',
          GPL:'blue',
          BSD:'yellow',
          CC:'blueviolet',
          Artistic:'important'
        }
    }
  },
  methods:{
    rowClick(row){
      console.log('row',row);
        this.$router.push({name:'Containerdetails',params:{id:row.ID}});
    },
    filterClick(index){
        for(let i in this.filters){
          this.filters[i].type = 'default';
        }

        this.filter = this.filters[index].name;
        this.filters[index].type = 'primary';

        /*
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
        }*/
    },
    sortClick(index){
          for(let i in this.sorts){
              if(i == index)
                this.sorts[i].type = 'primary';
              else
                this.sorts[i].type = 'default';
          }
    },
    search(){
        this.loading=true;
        this.dataFound=false;
        this.cardList=[];
        if(this.query.description)
          delete this.query.description;
        if(this.query.id)
          delete this.query.id;
        if(this.query.toolname)
          delete this.query.toolname;

        if(this.filter == 'Description')
         this.query.description = this.keywords;
        else if(this.filter == 'ID')
          this.query.id = this.keywords;
        else if(this.filter == 'Name')
          this.query.toolname = this.keywords;
        else if(this.filter == 'All'){
          this.query['all_fields_search'] = this.keywords;
        }
        this.$http
            .get(this.$store.state.baseApiURL + '/api/ga4gh/v2/tools',{params:this.query})
            .then(function(res){
              console.log(res);
              let tempLength = res.body.length;
              if(tempLength > 0){
                  let limit = res.headers.map.last_page[0].split('&')[0].split('=')[1];
                  let offset = res.headers.map.last_page[0].split('&')[1].split('=')[1];
                  this.total = parseInt(limit)+parseInt(offset);
                  this.dataFound=true;
                  for(let i=0; i<tempLength; i++){
                      var item = {
                        id:res.body[i].id,
                        toolname:res.body[i].toolname.toUpperCase(),
                        description:res.body[i].description ? res.body[i].description:'Tool description is coming',
                        tags:['tag1','tag2','tag2'],
                        state:'',
                        color:res.body[i].verified ? '#19be6b': '#c5c8ce',
                        license:''
                      };
                      let found=false;
                      for(let j in this.licenseColor){
                        if(res.body[i].license&&res.body[i].license.match(j)){
                          console.log(res.body[i].license);
                          console.log(encodeURIComponent(res.body[i].license));
                          item.license = 'https://img.shields.io/badge/license-'+encodeURIComponent(res.body[i].license).replace(/-/g,'--') + '-'+ this.licenseColor[j]+'.svg';
                          found=true;
                          break;
                        }
                      }
                      if(res.body[i].license&&!found){
                        console.log(res.body[i].license);
                        console.log(encodeURIComponent(res.body[i].license));
                        item.license = 'https://img.shields.io/badge/license-'+encodeURIComponent(res.body[i].license).replace(/-/g,'--') + '-lightgrey.svg';
                      }
                      this.cardList.push(item);
                  }
              }
              else{
                this.dataFound=false;
              }
              this.loading=false;
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
    pageChange(page){
      this.current=page;
      this.query.offset = parseInt(this.pageSize) * (parseInt(page)-1) + 1;
      console.log(page,this.pageSize,this.query.offset);
      this.search();
    },
    pageSizeChange(pageSize){
      this.pageSize = pageSize;
      this.query.limit = this.pageSize;
      this.search();
    },
    gotoContainerDetails(id){
      console.log('ididididid',id);
      //this.$router.push({name:'dataset',params:{id:id}});
      this.$router.push({name:'tools',params:{id:id}});
    },
  },
  mounted(){
    this.search();
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
      margin-bottom: 30px;
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
    .card-content-wrapper .left{
      display: flex;
      justify-content: space-between;
      overflow: hidden;
      /* text-overflow: ellipsis; */
      white-space: normal;
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
      width: 100%;
      text-align:justify;
    }
    .tag-wrapper{
      margin-bottom: 5px;
      display: inline-block;
    }
    .card{
      display: inline-block;
      margin: 0 15px;
      margin-bottom: 30px;
      height: 200px;
      min-height: 200px;
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
    .tool-name{
      /*
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: normal;*/
    }
    .license-img{
      position: absolute;
      bottom: 10px;
      right: 10px;
    }
    @media (max-width: 840px) {
      .card{
        width: calc((100% - 0px) / 1 - 3px);
        margin-left: 0 !important;
        margin-right: 0 !important;
      }
    }
    @media (max-width: 1015px) and (min-width: 841px){
      .card{
        width: calc((100% - 60px) / 2 - 3px);

      }
      .container-wrapper{
        margin-left: -15px;
        margin-right: -15px;
      }
    }
    @media (max-width: 1510px) and (min-width: 1016px){
      .card{
        width: calc((100% - 90px) / 3 - 4px);
      }
      .container-wrapper{
        margin-left: -15px;
        margin-right: -15px;
      }
    }
    @media (max-width: 3910px) and (min-width: 1511px){
      .card{
        width: calc((100% - 120px) / 4 - 4px);
      }
      .container-wrapper{
        margin-left: -15px;
        margin-right: -15px;
      }
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
    .description-wrapper textarea{
      resize: none !important;
      outline: none !important;
      border:none !important;
    }
    .description-wrapper .ivu-input{
      border: none !important;
      cursor: default;
    }
    .description-wrapper .ivu-input[disabled]{
      background: none;
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
