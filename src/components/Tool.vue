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
            <Row :gutter="16">
                <Tabs v-model="tabName">
                    <TabPane label="Readme" icon="ios-list-box" name="readme">
                        <Row :gutter="80">
                             <Col span="16">
                                  <div style="margin-bottom: 20px">
                                      <div class="title-container">{{containerObj.name}}</div>
                                      <div class="description-container" v-if="!containerObj.isMultiTool">{{containerObj.description}}</div>
                                      <div class="description-container" v-if="containerObj.isMultiTool">
                                          <div>This is a multitool container and package, a container that contains multiple bioinformatics tools. The contains the following tools:</div>
                                          <div>
                                              <a v-for="tool in containerObj.tools" v-bind:href="tool.url">
                                                  <img v-bind:src="tool.image" />
                                              </a>
                                          </div>
                                          <div><br></div>
                                      </div>
                                      <div></div>
                                      <div>
                                          <img v-if="containerObj.conda===true" src="https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square&logo=anaconda" />
                                          <img v-if="containerObj.docker===true" src="https://img.shields.io/badge/install%20with-docker-important.svg?style=flat-square&logo=docker" />
                                          <img v-if="containerObj.singularity===true" src="https://img.shields.io/badge/install%20with-singularity-blue.svg?style=flat-square" />
                                      </div>
                                  </div>
                                  <div class="middle" style="margin-bottom: 20px">
                                      <div><h2>Usage</h2></div>
                                      <Divider class="divider"/>
                                      <div>
                                          <div v-if="containerObj.conda===true" class="description-container">
                                              <div><strong>BioConda Installation</strong></div>
                                              <div>With an activated BioConda channel (see <a href="https://bioconda.github.io/user/install.html#set-up-channels">Set up bioconda channels</a>), install with:</div>
                                              <div class="code">conda install {{containerObj.name}}</div>
                                              <div></div>
                                              <div>More information about BioConda can be found <a href="https://bioconda.github.io/user/index.html">here</a></div>
                                              <div></div>
                                              <div><strong>Install specific version</strong></div>
                                              <div>From the Packages and Containers tab you can select a conda package version to install: </div>
                                              <div class="code">{{containerObj.conda_example}}</div>
                                              <div></div>
                                              <div><strong>Update to latest version</strong></div>
                                              <div>You can update your package to the latest version using the following command:</div>
                                              <div class="code">conda update {{containerObj.name}}</div>
                                          </div>
                                          <div v-if="containerObj.docker===true" class="description-container">
                                              <div><strong>Docker Installation</strong></div>
                                              <div>You first need to be sure that <a href="https://biocontainers-edu.readthedocs.io/en/latest/getting_started.html">docker is installed in your system</a>, then you can install the containers using the following command:</div>
                                              <div class="code">{{containerObj.docker_example}}</div>
                                              <div></div>
                                              <div>For docker containers no latest version is available, you always need to use the container tag.</div>
                                          </div>
                                          <div v-if="containerObj.singularity===true" class="description-container">
                                              <div><strong>Singularity Installation</strong></div>
                                              <div>You first need to be sure that <a href="https://sylabs.io/guides/3.5/user-guide/quick_start.html#quick-installation-steps">singularity is installed in your system</a>, then you can use the containers using the following command:</div>
                                              <div class="code">{{containerObj.singularity_example}}</div>
                                              <div></div>
                                              <div>For docker containers no latest version is available, you always need to use the container tag.</div>
                                          </div>
                                      </div>
                                  </div>
                                  <div class="foot">
                                      <div><strong>Keyword</strong></div>
                                      <Divider class="divider"/>
                                      <div class="tag-button-wrapper" >
                                          <Button v-for="item in containerObj.keywords" v-bind:key="item" style="margin-right:5px;height:30px;font-size:16px;line-height:30px; background: #f90; padding: 0 8px;" @click="search(item)">{{item}}</Button>
                                      </div>
                                  </div>
                             </Col>
                             <Col span="8">
                                  <div class="property-container">
                                      <div class="property-wrapper">
                                        <div class="property-item">
                                            <div class="property-title"><strong>Downloads</strong></div>
                                            <div class="property-content">{{containerObj.pulls}}</div>
                                        </div>
                                      </div>
                                      <Divider class="divider" v-if="!containerObj.isMultiTool"/>
                                      <div class="property-wrapper" v-if="!containerObj.isMultiTool">
                                        <div class="property-item">
                                            <div class="property-title"><strong>Homepage</strong></div>
                                            <div class="property-content"><a v-bind:href="containerObj.url" target="_blank">{{containerObj.url}}</a></div>
                                        </div>
                                      </div>
                                      <Divider class="divider" v-if="!containerObj.isMultiTool"/>
                                      <div class="property-wrapper">
                                        <div class="property-item" v-if="!containerObj.isMultiTool">
                                            <div class="property-title"><strong>Versions</strong></div>
                                            <read-more more-str="" v-bind:text="containerObj.versions_text" link="#" less-str="" :max-chars="50"></read-more>
                                        </div>
                                        <div class="property-item" v-if="!containerObj.isMultiTool">
                                            <div class="property-title"><strong>License</strong></div>
                                            <div class="property-content"><img class="license-img2" :src="containerObj.license"/></div>
                                        </div>
                                      </div>
                                      <Divider class="divider" v-if="!containerObj.isMultiTool"/>
                                      <div class="property-wrapper" v-if="!containerObj.isMultiTool">
                                        <div>
                                            <div class="property-title"><strong>GitHub Repo</strong></div>
                                            <div v-if="containerObj.github_repo">
                                                <gh-btns-watch v-bind:slug="containerObj.github_repo" show-count/>
                                                <gh-btns-star v-bind:slug="containerObj.github_repo" show-count/>
                                                <gh-btns-fork v-bind:slug="containerObj.github_repo" show-count/>
                                            </div>
                                        </div>
                                      </div>
                                      <Divider class="divider"/>
                                      <div class="property-wrapper">
                                        <div class="property-item">
                                            <div class="property-title"><strong>Last Update</strong></div>
                                            <div class="property-content">{{containerObj.last_update}}</div>
                                        </div>
                                      </div>
                                      <Divider class="divider" v-if="!containerObj.isMultiTool && containerObj.identifiers.length > 0"/>
                                      <div class="property-wrapper" v-if="!containerObj.isMultiTool && containerObj.identifiers.length > 0">
                                        <div class="property-item" v-if="!containerObj.isMultiTool">
                                            <div class="property-title" v-if="!containerObj.isMultiTool && containerObj.identifiers.length > 0"><strong>Identifiers</strong></div>
                                            <div class="property-content" v-if="containerObj.identifiers && !containerObj.isMultiTool">
                                                <ul>
                                                    <li v-for="menuItem in containerObj.identifiers" class="nav-item">
                                                        <a :href="menuItem.url" class="nav-link" target='_blank'>{{ menuItem.text }}</a>
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                      </div>
                                  </div>
                             </Col>
                        </Row>
                    </TabPane>
                    <TabPane label="Packages and Containers" icon="logo-buffer" name="package">
                        <Table class="tool-table" :columns="resultsTableCol" :data="containerObj.images"></Table>
                    </TabPane>
                    <TabPane label="Similar Tools" icon="ios-apps" name="similar" :disabled="similarNotFound">
                        <div class="container-wrapper">

                            <Card v-for="item in similarProjects" class="card" v-bind:key="item.id">
                                <p slot="title"><a class="tool-name" @click="gotoDetails(item.id)">{{item.name}}</a></p>
                                <p style="display: flex" slot="extra">
                                    <span>
                                        <Icon type="md-cloud-download" size="22"/>
                                    </span>
                                    <span style="padding-top: 1px; margin-left: 2px">
                                        {{item.pulls}}
                                    </span>
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
                        </div>
                    </TabPane>

                </Tabs>
            </Row>
          </div>
      </div>
      <Modal
          title="Security"
          v-model="showModal"
          name="Security"
          :closable="false"
          @on-ok="modalClose">
          <Table border ref="addPropertyTable" class="add-col-table" :columns="tableCols" :data="tableData" height="500"></Table>
      </Modal> 
  </div>
</template>

<script>
import Vue from 'vue';
import 'vue-github-buttons/dist/vue-github-buttons.css'; // Stylesheet
import VueGitHubButtons from 'vue-github-buttons'; // Component plugin
Vue.use(VueGitHubButtons, { useCache: true });

var gh = require('parse-github-url');

import store from "@/store/store.js"

function retrieveURL(identifier) {
    let url = ''
    if (identifier.indexOf('biotools') != -1){
        url = 'https://bio.tools/' + identifier.replace('biotools:', '')
    }
    if(identifier.indexOf('PMID') != -1){
        url = 'https://pubmed.ncbi.nlm.nih.gov/' + identifier.replace('PMID:', '')
    }
    return url
}

// import VulnerabilitiesModal from './VulnerabilitiesModal'
export default {
  name: 'tools',
  components: {
    // VulnerabilitiesModal: VulnerabilitiesModal
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
            versions_text:'',
            images:[],
            similars:[],
            conda: false,
            docker: false,
            singularity: false,
            identifiers: [],
            isMultiTool: false,
            tools: []

        },
        loading:true,
        dataFound:false,
        filter:'All',
        resultsTableCol:[

            {
                title: 'Type',
                key: 'type',
                align: 'center',
                width: 95,
                sortable: true,
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
                title: 'Version',
                key: 'version',
                align: 'center',
                sortable: true,
                width: 110,
            },
            {
                title: 'Last Update',
                key: 'last_updated',
                align: 'center',
                sortable: true,
                width: 140,
            },
            {
                title: 'Size',
                key: 'size',
                align: 'center',
                sortable: true,
                width: 100,
            },
            {
                title: 'Full Tag',
                key: 'full_tag',
                sortable: true,
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
                                          size: '24'
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
                title: 'Security',
                key: 'security',
                align: 'center',
                width: 100,
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
                                          type: 'ios-link',
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
        similarTableCol:[
            {
                title: 'Name',
                key: 'name',
                sortable: true,
            },
            {
                title: 'Description',
                key: 'description',
                sortable: true,
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
        similarProjects:[],
        tabName:'readme',
        tableCols: [
            {
                title: 'Feed',
                key: 'feed_group',
                align: 'center',
            },
                        {
                title: 'Package',
                key: 'package',
                align: 'center',
                sortable: true,
            },
            {
                title: 'Severity',
                key: 'severity',
                align: 'center',
                sortable: true,
            },
            {
                title: 'CVE',
                key: 'vuln',
                align: 'center',
                sortable: true,
            },
        ],
        tableData:[],
        similarNotFound: false,
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
      console.log('row',container)
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
              this.$Notice.error({
                  title: 'Image Check Error',
                  desc: 'Not analysed yet'
              });
            })
    },
    getVulnerabilities(digest) {
      let ctx = this;
        this.$http
            .get('https://jenkins.biocontainers.pro/security/v1/images/' + digest + '/vuln/all')
            .then(function (res) {
              this.showModal = true
              
              this.tableData = res.body.vulnerabilities
              console.log('this.tableData',res.body.vulnerabilities)
              // ctx.$modal.show('vulnerabilities', {vulnerabilities: res.body.vulnerabilities, msg: ''})
              
            }).catch(function(err) {

            })
    },
    toolInfo(id){
        console.log('this.$router.params.id',id)
        this.$http
            .get(this.$store.state.baseApiURL + '/ga4gh/trs/v2/tools/'+ id)
            .then(function (res) {
                console.log('res.body', res.body);
                let resbody = res.body;
                this.containerObj = {
                    name:res.body.name,
                    license:'',
                    url: resbody.tool_url,
                    description: resbody.description,
                    pulls: abbreviateNumber(resbody.pulls),
                    // url: resbody.url,
                    versions:'',
                    images:[],
                    keywords:resbody.tool_tags,
                    identifiers: []
                };
                let parse_url = gh(this.containerObj.url);
                if (parse_url !== null){
                    this.containerObj.github_repo = parse_url.path
                }

                console.log('this.containerObj',this.containerObj)
                let found=false;
                let versions = []
                for(let j in this.licenseColor){
                    if(resbody.license&&resbody.license.match(j)){
                      this.containerObj.license = 'https://img.shields.io/badge/license-'+encodeURIComponent(resbody.license).replace(/-/g,'--') + '-'+ this.licenseColor[j]+'.svg?style=flat-square';
                      found=true;
                      break;
                    }
                }
                if(resbody.license&&!found){
                    this.containerObj.license = 'https://img.shields.io/badge/license-'+encodeURIComponent(resbody.license).replace(/-/g,'--') + '-lightgrey.svg?style=flat-square';
                }
                for(let i = 0; i < resbody.versions.length; i++){
                    let current_version = resbody.versions[i]
                    var version_item = {
                        tool: current_version.name,
                        version: current_version.meta_version
                    };
                    versions.push(current_version.meta_version);
                }
                versions.sort();
                versions.reverse();
                this.containerObj.versions_text = versions.join(', ')
                console.log('versions', this.containerObj.versions_text)

                for(let i = 0; i < resbody.identifiers.length; i++){
                    let identifier = resbody.identifiers[i]
                    var item = {
                        text: identifier,
                        url: retrieveURL(identifier)
                    };
                    this.containerObj.identifiers.push(item);
                }

            //    If the containers is a mulled container.
                 this.containerObj.tools = []
                if (this.containerObj.name.indexOf('mulled-') !== -1){
                    this.containerObj.isMultiTool = true

                    for(let i = 0; i < resbody.contains.length; i++){
                        let tool = resbody.contains[i]
                        var item = {
                            image: 'https://img.shields.io/static/v1?label=included%20tool&message=' + tool +'&color=yellow',
                            url: "https://biocontainers.pro/#/tools/" + tool
                        };
                        this.containerObj.tools.push(item);
                    }
                }

            })

    },
    containerID(id){
         this.$http
            .get(this.$store.state.baseApiURL + '/ga4gh/trs/v2/tools/'+ id +'/versions')
            .then(function(res){
                console.log('res.body',res.body);
                let resbody=res.body[0];
                this.containerObj.images=[]
                let all_versions = res.body;
                this.containerObj.conda = false
                this.containerObj.docker = false
                this.containerObj.singularity = false
                this.containerObj.last_update = ''
                let original_type = "/static/images/docker.png";
                let prefix = 'docker pull ';
                this.containerObj.docker_example = ''
                for(let j = 0 ; j < all_versions.length; j++){
                    let current_version = all_versions[j];
                    for(let i=0; i < current_version.images.length; i++){
                        if(current_version.images[i].image_type === 'Docker' || (current_version.images[i].image_type !== 'Conda' && current_version.images[i].image_name.indexOf('depot.galaxyproject.org') === -1)){
                            original_type = "/static/images/docker.png";
                            prefix = 'docker pull ';
                            this.containerObj.docker = true
                            this.containerObj.docker_example = prefix + current_version.images[i].image_name
                        }
                        if(current_version.images[i].image_type === 'Conda'){
                            original_type = "/static/images/conda.png";
                            prefix = 'conda install -c conda-forge -c bioconda ';
                            this.containerObj.conda = true
                            this.containerObj.conda_example = prefix + current_version.images[i].image_name
                        }
                        if(current_version.images[i].image_type === 'Singularity' || current_version.images[i].image_name.indexOf('depot.galaxyproject.org') !== -1){
                            this.containerObj.singularity = true
                            original_type = "/static/images/singularity.png"
                            prefix = 'singularity run '
                            this.containerObj.singularity_example = prefix + current_version.images[i].image_name
                        }
                        var item = {
                            tool: current_version.name,
                            version: current_version.meta_version,
                            full_tag: prefix + current_version.images[i].image_name,
                            size: (current_version.images[i].size/1048576).toFixed(2) + "M",
                            last_updated: current_version.images[i].hasOwnProperty('updated')? current_version.images[i].updated.substring(0,10): '',
                            type: original_type,
                            full_version: current_version.images[i].image_name
                        };
                        this.containerObj.images.push(item);
                        if(item.last_updated > this.containerObj.last_update){
                            this.containerObj.last_update = item.last_updated
                        }
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
      
      this.$router.push({name:'tools',params:{id:id}})
      this.tabName ='readme'
    },
    getSimilars(id){
        this.$http
            .get(this.$store.state.baseApiURL + '/ga4gh/trs/v2/tools/'+ id + '/similars')
            .then(function (res) {
                // console.log('res.body similars', res.body);
                this.similarProjects = []
                let resbody = res.body;
                resbody = resbody.sort((a, b) => (a.similar_score < b.similar_score) ? 1 : -1)
                for(let i = 0; i < resbody.length; i++){
                    var item = {
                        id: resbody[i].id,
                        description: resbody[i].description,
                        name: resbody[i].name,
                        license: resbody[i].license,
                        pulls: abbreviateNumber(resbody[i].pulls),
                    };
                    let found=false;
                      for(let j in this.licenseColor){
                        if(resbody[i].license&&resbody[i].license.match(j)){
                          item.license = 'https://img.shields.io/badge/license-'+encodeURIComponent(resbody[i].license).replace(/-/g,'--') + '-'+ this.licenseColor[j]+'.svg';
                          found=true;
                          break;
                        }
                      }
                      if(res.body[i].license&&!found){
                        item.license = 'https://img.shields.io/badge/license-'+encodeURIComponent(resbody[i].license).replace(/-/g,'--') + '-lightgrey.svg';
                      }
                    this.similarProjects.push(item);
                }
                if (this.similarProjects.length == 0){
                  this.similarNotFound = true
                }
            })

    },
    modalClose(){

    },
    search(item){
      this.$router.push({name: 'Registry', query: {all_fields_search:item,sort_order:'asc',sort_field:'default',offset:0,limit:30}});
    }
  },
  beforeRouteUpdate (to, from, next) {
     this.toolInfo(to.params.id);
     this.containerID(to.params.id);
     this.getSimilars(to.params.id);
     next();
  },
  mounted(){
    this.toolInfo(this.$route.params.id);
    this.containerID(this.$route.params.id);
    this.getSimilars(this.$route.params.id);
  }
}

var SI_SYMBOL = ["", "K", "M", "G", "T", "P", "E"];

function abbreviateNumber(number){

    // what tier? (determines SI symbol)
    var tier = Math.log10(number) / 3 | 0;

    // if zero, we don't need a suffix
    if(tier === 0) return number;

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
    .ivu-table{
        font-size: 14px;
    }
    .ivu-tag{
        font-size: 16px;
    }
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
        font-size: 20px;
        font-weight: 700;
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
    .tag-button-wrapper button:hover{
      opacity: 0.8;
      color: #747b8b;
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
    .license-wrapper{
      display: flex;
      align-items: center;
    }
    .license-img2{
      /*margin-left: 10px;*/
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
    .property-wrapper{
      display: flex;
      /*margin-bottom: 10px;*/
      width: 100%;
    }
    .property-item{
      width: 50%
    }
    .divider{
      margin:10px 0;
    }
    .middle .code{
        background: #EEE;
        padding: 5px 20px;
        display: inline-block;
        width: 100%;
        font-size: 14px;
        font-family: "Anonymous Pro", "Menlo", "Consolas", "Bitstream Vera Sans Mono", "Courier New", monospace;
    }
    .description-container div{
      margin-bottom: 10px;
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
    .tool-table .ivu-table{
      font-size: 14px;
    }
    .tool-table .ivu-tag{
      font-size: 14px;
    }
</style>
