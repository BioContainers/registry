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
            <!-- <Input v-model="keywords" icon="ios-search" placeholder="Search" style="width:100%" @on-enter="addKeyword"/> -->
            <Input v-model="keywords" icon="ios-search" placeholder="Search" style="width:100%" @on-enter="submitSearch"/>
          </div>
          <div class="search-options-wrapper">
              <div class="filter-wrapper">
<!--                  <div class="filter">-->
<!--                        <span class="name">Filters:</span>-->
<!--                        <ButtonGroup>-->
<!--                            <Button class="filter-button" v-for="(item ,index) in filters" :type="item.type" :key="index" @click="filterClick(index)">{{item.name}}</Button>-->
<!--                        </ButtonGroup>-->
<!--                  </div>-->
                  <div class="sort">
                        <span class="name">Sorts by:</span>
                        <div class="sortOption">
                            <Select v-model="sortType" style="width:90px" @on-change="sortTypeClick">
                                <Option v-for="item in sortTypeArray" :value="item.value" :key="item.value">{{ item.label }}</Option>
                            </Select>
                        </div>
                  </div>
                  <div class="sort">
                        <span class="name">Sorts Order:</span>
                        <div class="sortOption">
                            <Select v-model="sortOrder" style="width:90px" @on-change="sortOrderClick">
                                <Option v-for="item in sortOrderArray" :value="item.value" :key="item.value">{{ item.label }}</Option>
                            </Select>
                        </div>
                  </div>
                  <div class="sort">
                        <span class="name">Refine Results:</span>
                        <div class="sortOption">
                            <Select v-model="facetName" style="width:90px" @on-change="facetNameChange"> 
                                <Option v-for="item in facetNameArray" :value="item" :key="item">{{item}}</Option>
                            </Select>
                            <Icon type="ios-arrow-forward" style="font-size: 12px"/>
                            <Select class="facet-value-select" v-model="facetValue" style="width:150px;position: relative;" @on-change="facetValueChange" filterable>
                                <Option v-for="item in facetValueArray" :value="item.value" :key="item.value">{{ item.value }} ({{item.count}})</Option> 
                            </Select>
                        </div>
                  </div>
              </div>
              <div class="search-button-wrapper">
                  <Button type="primary" @click="submitSearch">Search</Button>
              </div>
          </div>
          <div class="tag-wrapper" style="margin-top: 10px;" >
            <Tag v-for="item in tagsArray" type="border" :color="item.value?'warning':'primary'" :key="item.name+item.value" :name="item.name+item.value" closable @on-close="removeFacetTag">{{item.name}}<span v-if="item.value">-></span>{{item.value}}</Tag>
          </div>
          <div class="container-wrapper">

                  <Spin fix v-if="loading"></Spin>

                  <div v-if="dataFound">
                  <Card v-for="item in cardList" class="card" v-bind:key="item.id">
                      <p slot="title"><a class="tool-name" @click="gotoContainerDetails(item.id)">{{item.toolname}}</a></p>
                      <p style="display: flex" slot="extra">

                        <span>
                            <Icon type="md-cloud-download" size="22"/>
                            <!--<div class="tooltip-content" slot="content">-->
                                <!--{{item.content}}-->
                            <!--</div>-->

                        </span>
                          <span style="padding-top: 1px; margin-left: 2px">
                                {{item.pulls}}
                            </span>
                      </p>
                      <div class="card-content-wrapper">
                        <div class="left">
                            <div class="description-wrapper">
                              <!--<Input v-model="item.description" disabled type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="" />-->
                              <read-more v-if="!item.multiTool" more-str="" :text="item.description" link="#" less-str="read less" :max-chars="120"></read-more>
                              <img v-if="!item.multiTool" class="license-img" :src="item.license"/>
                              <div v-if="item.multiTool">
                                  <div>This is a multitool container. The following tools are part of the container:</div>
                                  <div>
                                      <a v-for="tool in item.contains" v-bind:href="tool.url" v-bind:key="tool.url">
                                          <img  v-bind:src="tool.image" />
                                      </a>
                                  </div>
                              </div>
                            </div>
                            <div class="state-wrapper">
                                {{item.state}}
                            </div>
                        </div>
                        <div class="right">
                        </div>
                      </div>
                  </Card>
                  </div>
                  <div v-if="!firstSearchState" class="no-data-container">
                      Input the keyword for search...
                  </div>
                  <div v-else>
                       <div v-if="!dataFound" class="no-data-container">
                          No matched Data
                      </div>
                  </div>
          </div>
          <div class="page-wrapper">
              <Page :total="total" :current="page" :page-size="pageSize" size="small" show-elevator show-sizer @on-change="pageChange" @on-page-size-change="pageSizeChange"/>
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
        total:0,
        page:1,
        pageSize:30,
        cardList:[],
        loading:false,
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
        sortType:'default',
        sortTypeArray:[
            {
                label:'Default',
                value:'default',
            },
            {
                label:'Pull No',
                value:'pulls',
            },
        ],
        sortOrder:'asc',
        sortOrderArray:[
            {
                label:'Asc',
                value:'asc',
            },
            {
                label:'Desc',
                value:'desc',
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
        facetNameArray:[],
        facetValueArray:[],
        facetValue:'',
        facetName:'',
        tagsArray:[],
        firstSearchState:false
    }
  },
  beforeRouteUpdate:function (to, from, next) {
        console.debug('beforeRouteUpdate',to.query)
        this.updateCondition(to.query)
        this.search(to.query);
        next();
    },
  methods:{
    rowClick(row){
      console.debug('row',row);
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
    sortTypeClick(index){
      console.debug(this.sortType)
      // this.query.sort_field = this.sortType
      // this.$router.push({name: 'Registry', query: this.query});
      // this.search();
        
      
    },
    sortOrderClick(index){
      // this.query.sort_order = this.sortOrder 
      // this.$router.push({name: 'Registry', query: this.query});
      // this.search();
    },
    submitSearch(){
      console.debug('submitSearch')
      this.firstSearchState = true
      this.$router.push({name: 'Registry', query: this.query});
      
    },
    updateCondition(q){
          console.debug('updateCondition',this.$route.query)
          let query = q || this.$route.query;
          let offsetFound = false
          let limitFound = false
          let sortfieldFound = false
          let sortOrderFound = false
          let keywordFound = false
          for(let i in query){
              if(i == 'all_fields_search' || i == 'description' || i == 'id' || i == 'toolname'){
                 keywordFound = true
                 this.keywords = query[i]
              }
              else if(i =='offset'){
                offsetFound = true
                try{
                  this.page= Math.round((parseInt(query['offset'])-1)/parseInt(query['limit'])) + 1;
                  console.debug('this.page',this.page)
                }
                catch(e){
                  this.page=1
                }
                //console.log(this.currentPage );
              }
              else if(i =='limit'){
                  limitFound = true
                  let tempPageSize = parseInt(query[i]);
                  if(tempPageSize == 10 || tempPageSize == 20 || tempPageSize == 30 || tempPageSize == 40)
                    this.pageSize = parseInt(query[i]);
                  else 
                    this.pageSize = 20;
              }
              else if(i =='sort_field'){
                console.debug('query',query)

                console.debug('sort_field found',query[i])
                sortfieldFound = true
                this.sortType = query[i]
                console.debug('this.sortType',this.sortType)
              }
              else if(i =='sort_order'){ 
                sortOrderFound = true
                this.sortOrder = query[i]         
              }
              else if(i == 'facets'){
                if(query[i]){
                  this.tagsArray = []
                  let filterArray = query[i].split(',');
                  for(let i=0; i<filterArray.length;i++){
                      let facetsArray = filterArray[i].split(':')
                      let item = {
                        name:facetsArray[0],
                        value:facetsArray[1],
                      }
                      this.tagsArray.push(item)
                  }
                }
                this.facets = query[i]
                console.debug('ready to get facets',query[i])
              }
          }
          // if(!keywordFound)
          //     this.keywords = '';
          // if(!sortOrderFound)
          //     this.sortOrder = 'asc'
          // if(!sortfieldFound)
          //     this.sortType = 'default'  
          // if(!limitFound)
          //     this.pageSize = 20;
          // if(!offsetFound)  
          //     this.page = 1;
      },
    search(q){
      return new Promise((resolve, reject) => {
        this.loading=true;
        this.dataFound=false;
        this.cardList=[];
        let query = q || this.$route.query;

        if(query.description)
          delete query.description;
        if(query.id)
          delete query.id;
        if(query.toolname)
          delete query.toolname;

        if(this.filter == 'Description')
          query.description = this.keywords;
        else if(this.filter == 'ID')
          query.id = this.keywords;
        else if(this.filter == 'Name')
          query.toolname = this.keywords;
        else if(this.filter == 'All'){ // currently filter is always "All"
          query['all_fields_search'] = this.keywords;
        }

        query.sort_order = this.sortOrder
        query.sort_field = this.sortType
        console.debug('search',query)
        // this.$router.push({name: 'Registry', query: this.query});
        this.$http
            .get(this.$store.state.baseApiURL + 'ga4gh/trs/v2/tools',{params:query})
            .then(function(res){
              let tempLength = res.body.length;
              if(tempLength > 0){
                let pageelts = res.headers.map.last_page[0].split('&')
                let limit=0;
                let offset=0;
                for(let e=0;e<pageelts.length;e++) {
                  let pageelt = pageelts[e].split('=');
                  if (pageelt[0] == 'limit') {
                    limit = pageelt[1]
                  } else if (pageelt[0] == 'offset') {
                    offset = pageelt[1]
                  }
                }
                  //let limit = res.headers.map.last_page[0].split('&')[0].split('=')[1];
                  //let offset = res.headers.map.last_page[0].split('&')[1].split('=')[1];
                  this.total = parseInt(limit)+parseInt(offset);
                  this.dataFound=true;
                  this.facetValue = '' //clear the faceValue Input
                  for(let i=0; i<tempLength; i++){
                      var item = {
                        id:res.body[i].id,
                        toolname:res.body[i].name,
                        description:res.body[i].description ? res.body[i].description:'Tool description is coming',
                        tags:['tag1','tag2','tag2'],
                        state:'',
                        pulls:abbreviateNumber(res.body[i].pulls),
                        color:res.body[i].verified ? '#19be6b': '#c5c8ce',
                        license:'',
                        multiTool: false,
                        contains: [],
                        contains_text: ''
                      };

                      if(item.toolname.indexOf('mulled-') !== -1){
                          item.multiTool = true
                          if (res.body[i].contains !== null){
                              for(let j = 0; j <res.body[i].contains.length; j++){
                                  var container = {
                                          image: 'https://img.shields.io/static/v1?label=included%20tool&message=' + res.body[i].contains[j] +'&color=yellow',
                                          url: "https://biocontainers.pro/#/tools/" + res.body[i].contains[j]
                                   };
                                  item.contains.push(container)
                              }
                          }
                      }
                      if(item.contains.length > 0)
                          item.contains_text = item.contains.join(', ')

                      let found=false;
                      for(let j in this.licenseColor){
                        if(res.body[i].license&&res.body[i].license.match(j)){
                          item.license = 'https://img.shields.io/badge/license-'+encodeURIComponent(res.body[i].license).replace(/-/g,'--') + '-'+ this.licenseColor[j]+'.svg';
                          found=true;
                          break;
                        }
                      }
                      if(res.body[i].license&&!found){
                        item.license = 'https://img.shields.io/badge/license-'+encodeURIComponent(res.body[i].license).replace(/-/g,'--') + '-lightgrey.svg';
                      }
                      this.cardList.push(item);
                  }
              }
              else{
                this.dataFound=false;
              }
              resolve();
              this.loading=false;
            },function(err){
                console.error('err',err);
                this.dataFound=false;
                this.loading=false;
                this.$Notice.error({
                    title: 'Server Error',
                    desc: err.body.error
                });
                reject();
            });
      });
    },
    pageChange(page){
      this.page=page;
      this.query.offset = parseInt(this.pageSize) * (parseInt(this.page)-1);
      console.debug('pageChange',page,this.pageSize,this.query.offset);
      this.$router.push({name: 'Registry', query: this.query});
      // this.search();
    },
    pageSizeChange(pageSize){
      this.pageSize = pageSize;
      this.query.limit = this.pageSize;
      this.$router.push({name: 'Registry', query: this.query});
      // this.search();
    },
    gotoContainerDetails(id){
      console.debug('ididididid',id);
      //this.$router.push({name:'dataset',params:{id:id}});
      this.$router.push({name:'tools',params:{id:id}});
    },
    getFacets(){
        this.$http
            .get(this.$store.state.baseApiURL + 'ga4gh/trs/v2/facets')
            .then(function(res){
              let tempLength = res.body.length;
              if(tempLength > 0){
                  this.facetObj = {}
                  this.facetName = res.body[0].facet
                  this.facetValueArray = res.body[0].values
                  for(let i in res.body){
                    let item = res.body[i]
                    this.facetNameArray.push(item.facet)
                    this.facetObj[item.facet] = item.values
                  }
                  // console.log('this.facetObj',res.body[0])
                  //this.updateCondition();
                  //this.search();
              }
              else{
                this.$Notice.error({
                    title: 'No facets: Server Error',
                    desc: err.body.error
                });
              }
            },function(err){
                console.error('err',err);
                this.$Notice.error({
                    title: 'No facets: Server Error',
                    desc: err.body.error
                });
            });
    },
    facetNameChange(val){
      console.debug('before facetNameChange',this.facetValue)
      this.facetValueArray = this.facetObj[val]
      this.facetValue=''
      console.debug('after facetNameChange',this.facetValue)
    }, 
    facetValueChange(val){
      for(let i in this.tagsArray){
        if(this.tagsArray[i].name == this.facetName && this.tagsArray[i].value == val){
          this.facetValue=''
          this.$Notice.error({
              title: 'Repeated Facets',
              desc: 'Do not add the repeated facets!'
          });
          return
        }
      }
      if(val){
          let item = {
            name:this.facetName,
            value:val
          }
          this.tagsArray.push(item)
          this.facetValue=''
      }
    },
    removeFacetTag(event, name){
      console.debug('name',name)
      for(let i in this.tagsArray){
        if((this.tagsArray[i].name+this.tagsArray[i].value) == name){
            this.tagsArray.splice(i, 1);
        }
      }
    },
      // addKeyword(){
      //   for(let i in this.tagsArray){
      //     if(this.tagsArray[i].name == this.keywords){
      //       this.$Notice.error({
      //           title: 'Repeated Keywords',
      //           desc: 'Do not add the repeated keywords!'
      //       });
      //       return
      //     }
      //   }
      //   if(this.keywords){
      //       let item = {
      //         name:this.keywords,
      //         value:''
      //       }
      //       this.tagsArray.push(item)
      //       this.keywords = ''
      //   }
      // }
  },
  watch:{
    tagsArray: function(val,oldVal){
          this.query.facets = ''
          for(let i in val){
            if(val[i].value){// it is a facet, if value is null, it is the keyword
              this.query.facets+=val[i].name+':'+val[i].value+','
            }
          }
          let reg=/,$/gi
          this.query.facets=this.query.facets.replace(reg,"");
          console.debug('watch',this.query.facets)
    },
  },
  computed:{
      //this variable is not used anymore and only for updating this.normalQuery;
      query:function(){
          let normalQuery = {}
          if(this.filter == 'Description')
            normalQuery.description = this.keywords;
          else if(this.filter == 'ID')
            normalQuery.id = this.keywords;
          else if(this.filter == 'Name')
            normalQuery.toolname = this.keywords;
          else if(this.filter == 'All'){ // currently filter is always "All"
            normalQuery['all_fields_search'] = this.keywords;
          }

          if(this.facets)
            normalQuery.facets = this.facets

          if(this.sortOrder)
            normalQuery.sort_order = this.sortOrder
          if(this.sortType)
            normalQuery.sort_field = this.sortType

          normalQuery.offset = parseInt(this.pageSize) * (parseInt(this.page)-1);
          normalQuery.limit = this.pageSize;
          return normalQuery;
      }
    },
  mounted(){
    console.debug('mounted')
    this.updateCondition();
    // this.search();
    this.getFacets();

  }
}

var SI_SYMBOL = ["", "K", "M", "G", "T", "P", "E"];

function abbreviateNumber(number){

    // what tier? (determines SI symbol)
    var tier = Math.log10(number) / 3 | 0;

    // if zero, we don't need a suffix
    if(tier == 0) return number;

    // get suffix and determine scale
    var suffix = SI_SYMBOL[tier];
    var scale = Math.pow(10, tier * 3);

    // scale the number
    var scaled = number / scale;

    // format number and add suffix
    return scaled.toFixed(1) + suffix;
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
    .sortOption{
      display: inline-block;
      position: relative;
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
    .facet-value-select .ivu-select-dropdown{
      max-width: 300px;
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
