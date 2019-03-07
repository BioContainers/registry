<template>
  <div class="index-container">
      <div class="first">
          <div class="first-body">
              <div class="container has-text-centered">
                  <img alt="BioContainers" style="width: 65%; margin-bottom: 36px;" src="https://proppyjs.com/img/banner-trimmed-900.png">

                  <h2 class="subtitle">
                    Tiny <span>1.5kB utility library</span> enabling
                  </h2>

                  <h1 class="title">
                    <span>Functional props composition for components</span>
                  </h1>

                  <div style="margin-bottom: 16px;">
                    <a href="/docs/introduction" class="button is-primary is-medium">Learn more</a>
                    <a href="/docs/quickstart" class="button is-transparent is-medium">Quick start</a>
                  </div>
              </div>
          </div>
      </div>
      <div class="second">
        <div class="second-body">
            <div class="container">
                 <p class="title">Flow of props</p>
                 <Row class="second-row">
                    <Col span="8">
                      <p>VARIOUS SOURCES</p>
                      <img style="height: 140px" src="https://proppyjs.com/img/redux-logo.png">
                    </Col>
                    <Col span="8">
                      <p>VARIOUS SOURCES</p>
                      <img style="height: 140px" src="https://proppyjs.com/img/redux-logo.png">
                    </Col>
                    <Col span="8">
                      <p>VARIOUS SOURCES</p>
                      <img style="height: 140px" src="https://proppyjs.com/img/redux-logo.png">
                    </Col>
                </Row>
            </div>
        </div>
      </div>
      <div class="third">
        <div class="third-body">
            <div class="container">
                 <p class="title">Benefits</p>
                 <Row class="third-row">
                    <Col span="8">
                      <div class="box">
                          <p class="title">Stateless</p>
                          <p class="sub-title">Your component layer ends up becoming stateless, and only responsible for accepting props and rendering them.</p>
                      </div>
                    </Col>
                    <Col span="8">
                      <div class="box">
                          <p class="title">Stateless</p>
                          <p class="sub-title">Your component layer ends up becoming stateless, and only responsible for accepting props and rendering them.</p>
                      </div>
                    </Col>
                    <Col span="8">
                      <div class="box">
                          <p class="title">Stateless</p>
                          <p class="sub-title">Your component layer ends up becoming stateless, and only responsible for accepting props and rendering them.</p>
                      </div>
                    </Col>
                </Row>
                <Row class="third-row">
                    <Col span="8">
                      <div class="box">
                          <p class="title">Stateless</p>
                          <p class="sub-title">Your component layer ends up becoming stateless, and only responsible for accepting props and rendering them.</p>
                      </div>
                    </Col>
                    <Col span="8">
                      <div class="box">
                          <p class="title">Stateless</p>
                          <p class="sub-title">Your component layer ends up becoming stateless, and only responsible for accepting props and rendering them.</p>
                      </div>
                    </Col>
                    <Col span="8">
                      <div class="box">
                          <p class="title">Stateless</p>
                          <p class="sub-title">Your component layer ends up becoming stateless, and only responsible for accepting props and rendering them.</p>
                      </div>
                    </Col>
                </Row>
            </div>
        </div>
      </div>
      <footer class="footer">
        <div class="container">
          <div class="content has-text-centered">
            <p>
              Built with ❤︎ by <a href="https://twitter.com/fahad19">@fahad19</a> and <a href="https://github.com/fahad19/proppy/graphs/contributors">contributors</a>.
            </p>

            <p class="social-icons">
              <a class="icon" title="GitHub" href="https://github.com/fahad19/proppy">
                <i class="fa fa-github"></i>
              </a>

              <a class="icon" title="Twitter" href="https://twitter.com/proppyjs">
                <i class="fa fa-twitter"></i>
              </a>

              <!--<a class="icon" title="Medium" href="https://medium.com/proppyjs">
                <i class="fa fa-medium"></i>
              </a>-->
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
      background: #e85166;
      text-align: left !important;
      margin:10px;
      padding: 20px;
    }
    .third-row .box .title{
      color: white;
      font-size: 32px;
      font-weight: 800;
    }
    .third-row .box .sub-title{
      color: white;
      font-size: 18px;
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
</style>

