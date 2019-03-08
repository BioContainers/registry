<template>
  <div class="index-container">
      <div class="first">
          <div class="first-body">
              <div class="container has-text-centered">
                  <img alt="BioContainers" style="width: 20%; margin-bottom: 36px;" src="static/images/containers.png">

                  <h2 class="subtitle">
                    BioContainers <span>Community</span>
                  </h2>

                  <h1 class="title">
                    <span>creating, maintaining and deploying software containers and workflows</span>
                  </h1>

                  <div style="margin-bottom: 16px; margin-top: 16px">
                    <a href="https://biocontainers-edu.biocontainers.pro" class="button">Quick Start</a>
                  </div>
              </div>
          </div>
      </div>
      <div class="second">
        <div class="second-body">
            <div class="container">
                 <p class="title">BioContainers Flow</p>
                 <Row class="second-row">
                    <Col span="8">
                      <p>SOFTWARE</p>
                      <img style="height: 140px" src="static/images/source-code.png">
                    </Col>
                    <Col span="8">
                      <p>CONTAINER</p>
                      <img style="height: 140px" src="static/images/container-2.png">
                    </Col>
                    <Col span="8">
                      <p>WORKFLOW</p>
                      <img style="height: 140px" src="static/images/workflow-2.png">
                    </Col>
                </Row>
            </div>
        </div>
      </div>
      <div class="third">
        <div class="third-body">
            <div class="container">
                 <!--<p class="title">Benefits</p>-->
                <Row class="third-row">
                    <Col span="8">
                      <div class="box">
                          <p class="title">Registry</p>
                          <p class="sub-title">List of bioinformatics containers and workflows including metadata, statistics</p>
                      </div>
                    </Col>
                    <Col span="8">
                      <div class="box">
                          <p class="title">tweets</p>
                          <p class="sub-title"></p>
                      </div>
                    </Col>
                    <Col span="8">
                      <div class="box">
                          <p class="title">How to Cite</p>
                          <p class="sub-title">da Veiga Leprevost F, Grüning BA, .. Perez-Riverol Y. Bioinformatics. 2017
                              Aug 15;33(16):2580-2582. <a href="https://academic.oup.com/bioinformatics/article/33/16/2580/3096437">BioContainers:
                                  an open-source and community-driven framework for software standardization</a></p>
                      </div>
                    </Col>
                </Row>
                <!--<Row class="third-row">-->
                    <!--<Col span="8">-->
                      <!--<div class="box">-->
                          <!--<p class="title">Stateless</p>-->
                          <!--<p class="sub-title">Your component layer ends up becoming stateless, and only responsible for accepting props and rendering them.</p>-->
                      <!--</div>-->
                    <!--</Col>-->
                    <!--<Col span="8">-->
                      <!--<div class="box">-->
                          <!--<p class="title">Stateless</p>-->
                          <!--<p class="sub-title">Your component layer ends up becoming stateless, and only responsible for accepting props and rendering them.</p>-->
                      <!--</div>-->
                    <!--</Col>-->
                    <!--<Col span="8">-->
                      <!--<div class="box">-->
                          <!--<p class="title">Stateless</p>-->
                          <!--<p class="sub-title">Your component layer ends up becoming stateless, and only responsible for accepting props and rendering them.</p>-->
                      <!--</div>-->
                    <!--</Col>-->
                <!--</Row>-->
            </div>
        </div>
      </div>
      <div class="second">
        <div class="second-body">
            <div class="container">
                 <p class="title">Partners</p>
                 <Row class="second-row">
                    <Col span="8">
                      <!--<p>BIOCONDA</p>-->
                      <a href="http://bioconda.github.io">
                          <img style="width: 180px" src="static/images/bioconda-2.png">
                      </a>
                    </Col>
                    <Col span="8">
                      <!--<p>NEXTFLOW</p>-->
                      <a href="http://nextflow.io">
                          <img style="width: 180px" src="static/images/nextflow.png">
                      </a>
                    </Col>

                     <Col span="8">
                      <!--<p>GA4GH</p>-->
                      <a href="https://www.ga4gh.org/">
                          <img style="width: 180px" src="static/images/ga4gh.png">
                      </a>
                    </Col>
                </Row>
                <div><br><br><br></div>
                <Row class="second-row">
                    <Col span="8">
                      <a href="https://www.commonwl.org/">
                          <img style="height: 85px" src="static/images/cwl-2.png">
                      </a>

                    </Col>
                    <Col span="8">
                      <!--<p>CWL</p>-->
                      <!--<img style="width: 180px" src="static/images/cwl-2.png">-->
                    </Col>
                    <Col span="8">
                      <!--<p>CWL</p>-->
                        <a href="https://galaxyproject.org/">
                             <img style="width: 180px" src="static/images/galaxy.png">
                        </a>
                    </Col>
                </Row>

            </div>
        </div>
      </div>
      <footer class="footer">
        <div class="container">
          <div class="content has-text-centered">
            <p>
              Built with ❤︎ by <a href="https://twitter.com/biocontainers">biocontainers</a>
            </p>

            <p class="social-icons">
              <a class="icon" title="GitHub" href="https://github.com/BioContainers">
                <i class="fa fa-github"></i>
              </a>

              <a class="icon" title="Twitter" href="https://twitter.com/biocontainers">
                <i class="fa fa-twitter"></i>
              </a>
            </p>
          </div>
        </div>
      </footer>
  </div>
</template>
<script>
export default {
  name: 'Index',
  data () {
    return {

    }
  },
  methods:{
    rowClick(row){

    },
  },
  mounted(){

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .first{
        width: 100%;
        background-color: #222836;
        color: #fff;
        margin: 0;
    }
    .first-body{
      padding-bottom: 1.5rem;
      padding-top: 1.5rem;
      text-align: center;
    }
    .first-body .subtitle{
      font-size: 24px;
    }
    .second{
      margin:40px 0;
    }
    .second-body{
        padding-bottom: 1.5rem;
        padding-top: 1.5rem;
    }
    .second-body .title{
        text-align: center;
        font-weight: 800;
        font-size: 54px;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    .second-row{
      text-align: center;
    }
    .second-row p{
      font-size: 16px;
      margin-bottom: 30px;
      font-weight: 600;
      text-transform: uppercase;
    }
    .third{
      margin:40px 0;
    }
    .third-body{
        padding-bottom: 1.5rem;
        padding-top: 1.5rem;
    }
    .third-body .container>.title{
        text-align: center;
        font-weight: 800;
        font-size: 54px;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    .third-row .box{
      background: #222836;
      text-align: left !important;
      margin:10px;
      padding: 20px;
    }
    .third-row .box .title{
      color: white;
      font-size: 20px;
      font-weight: 800;
    }
    .third-row .box .sub-title{
      color: white;
      font-size: 14px;
    }
    .container{
      margin:0 auto;
    }
    .footer {
      background-color: #fafafa;
      border-top: 1px solid #eee;
      padding: 3rem 1.5rem 3rem;
      position: relative;
    }
    .footer .content{
      text-align: center;
    }
    @media screen and (min-width: 1280px){
      .container {
          max-width: 940px;
          width: 940px;
      }
    }
    @media screen and (min-width: 1280px){
      .container {
          max-width: 1152px;
          width: 1152px;
      }
    }
    @media screen and (min-width: 1088px){
      .container {
          max-width: 960px;
          width: 960px;
      }
    }
    .first-body{
        padding-top: 6.5rem;
    }
    a.button{
        display:inline-block;
        padding:0.3em 1.2em;
        margin: 0em 0.1em 0.1em 0em;
        border: 0.06em solid rgba(255,255,255,1);
        border-radius:2em;
        box-sizing: border-box;
        text-decoration:none;
        font-family:'Roboto',sans-serif;
        font-weight:300;
        color: #FFFFFF;
        text-shadow: 0em 0.04em 0.04em rgba(0,0,0,0.35);
        text-align:center;
        transition: all 0.2s;
        font-size: 16px;
    }
    a.button:hover{
        border-color: rgba(255,255,255,3);
    }

    @media all and (max-width:30em){
        a.button{
             display:block;
            margin:0.2em auto;
        }
    }
</style>

