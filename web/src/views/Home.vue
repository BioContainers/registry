<template>
  <div class="index-container">
    <!-- Hero -->
    <div class="first">
      <div class="first-body">
        <div class="container has-text-centered">
          <img class="hero-img" src="/static/images/containers.png" alt="BioContainers" />
          <h2 class="subtitle">BioContainers</h2>
          <h1 class="title">
            <template v-if="stats">
              {{ stats.tools.toLocaleString() }} tools,
              {{ stats.versions.toLocaleString() }} versions,
              {{ (stats.containers || stats.versions).toLocaleString() }} containers and packages
            </template>
            <Spin v-else size="large" />
          </h1>
          <div class="cta">
            <a class="button" href="https://biocontainers-edu.readthedocs.io/en/latest/">Quick Start</a>
            <a class="button" @click="$router.push('/registry')">Registry</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Flow -->
    <div class="second">
      <div class="second-body">
        <div class="container">
          <p class="title">BioContainers Flow</p>
          <Row class="second-row" :gutter="16" align="middle" justify="center">
            <Col span="6">
              <p>SOFTWARE</p>
              <img class="flow-img" src="/static/images/source-code.png" alt="" />
            </Col>
            <Col span="2"><Icon type="md-arrow-round-forward" size="38" /></Col>
            <Col span="6">
              <p>CONTAINER</p>
              <img class="flow-img" src="/static/images/container-2.png" alt="" />
            </Col>
            <Col span="2"><Icon type="md-arrow-round-forward" size="38" /></Col>
            <Col span="6">
              <p>WORKFLOW</p>
              <img class="flow-img" src="/static/images/workflow-2.png" alt="" />
            </Col>
          </Row>
        </div>
      </div>
    </div>

    <!-- Main components -->
    <div class="third">
      <div class="third-body">
        <div class="container">
          <p class="title">Main Components</p>
          <Row class="third-row" :gutter="16">
            <Col span="8">
              <div class="box">
                <p class="title">Registry</p>
                <p class="sub-title">
                  List of bioinformatics containers and packages including metadata and statistics.
                </p>
                <a class="button dark" @click="$router.push('/registry')">Registry</a>
              </div>
            </Col>
            <Col span="8">
              <div class="box">
                <p class="title">Specifications</p>
                <p class="sub-title">
                  Specifications and architecture to create, deploy and maintain software
                  containers using Conda and Docker technologies.
                </p>
                <a class="button dark" href="https://biocontainers-edu.readthedocs.io/en/latest/what_is_biocontainers.html">Read More</a>
              </div>
            </Col>
            <Col span="8">
              <div class="box">
                <p class="title">Community</p>
                <p class="sub-title">
                  An open-source and community-driven framework for software standardization
                  built on Bioconda and BioContainers.
                </p>
                <a class="button dark" href="https://github.com/BioContainers">GitHub</a>
              </div>
            </Col>
          </Row>
        </div>
      </div>
    </div>

    <!-- Partners -->
    <div class="second">
      <div class="second-body">
        <div class="container">
          <p class="title">Partners</p>
          <Row class="second-row" :gutter="16" align="middle" justify="center">
            <Col span="8"><a href="http://bioconda.github.io"><img class="partner" src="/static/images/bioconda-2.png" alt="Bioconda" /></a></Col>
            <Col span="8"><a href="http://nextflow.io"><img class="partner" src="/static/images/nextflow.png" alt="Nextflow" /></a></Col>
            <Col span="8"><a href="https://www.ga4gh.org/"><img class="partner" src="/static/images/ga4gh.png" alt="GA4GH" /></a></Col>
          </Row>
          <br /><br />
          <Row class="second-row" :gutter="16" align="middle" justify="center">
            <Col span="8"><a href="https://www.commonwl.org/"><img class="partner tall" src="/static/images/cwl-2.png" alt="CWL" /></a></Col>
            <Col span="8"><a href="https://elixir-europe.org/"><img class="partner tall" src="/static/images/elixir.png" alt="ELIXIR" /></a></Col>
            <Col span="8"><a href="https://galaxyproject.org/"><img class="partner" src="/static/images/galaxy.png" alt="Galaxy" /></a></Col>
          </Row>
        </div>
      </div>
    </div>

    <!-- Documentation / Cite -->
    <div class="fourth">
      <div class="fourth-body">
        <div class="container">
          <Row class="fourth-row" :gutter="16">
            <Col span="12">
              <div class="box">
                <p class="title">Documentation</p>
                <p class="sub-title">
                  How to create a container, how to use it in a workflow — everything you need to
                  know about BioContainers.
                </p>
                <a class="button dark" href="https://biocontainers-edu.readthedocs.io/en/latest/">Documentation</a>
              </div>
            </Col>
            <Col span="12">
              <div class="box">
                <p class="title">How to Cite</p>
                <p class="sub-title">
                  da Veiga Leprevost F, Grüning BA, … Perez-Riverol Y. Bioinformatics. 2017;33(16):2580-2582.
                  <a href="https://academic.oup.com/bioinformatics/article/33/16/2580/3096437">BioContainers: an open-source and community-driven framework for software standardization</a>
                </p>
              </div>
            </Col>
          </Row>
        </div>
      </div>
    </div>

    <footer class="footer">
      <div class="container content has-text-centered">
        <p>Built with ❤︎ by <a href="https://github.com/BioContainers">biocontainers</a></p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { loadStats } from '../lib/dataClient.js'

const stats = ref(null)
onMounted(async () => {
  stats.value = await loadStats()
})
</script>

<style scoped>
.has-text-centered { text-align: center; }
.container { margin: 0 auto; max-width: 1100px; padding: 0 16px; }

.first { width: 100%; background-color: #222836; color: #fff; margin: 0; }
.first-body { padding: 6.5rem 0 3rem; text-align: center; }
.hero-img { width: 160px; margin-bottom: 32px; }
.first-body .subtitle { font-size: 24px; color: #c5c8ce; }
.first-body .title { color: #fff; font-size: 30px; font-weight: 600; margin: 16px 0 8px; border: none; }
.cta { margin-top: 24px; }

.second, .third, .fourth { margin: 48px 0; }
.second-body .title, .third-body .container > .title, .fourth-body .container > .title {
  text-align: center; font-weight: 800; font-size: 40px;
  border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 30px;
}
.second-row { text-align: center; }
.second-row p { font-size: 16px; margin-bottom: 20px; font-weight: 600; text-transform: uppercase; }
.flow-img { height: 130px; object-fit: contain; }
.partner { width: 170px; object-fit: contain; }
.partner.tall { height: 80px; width: auto; }

.third-row .box { background: #222836; text-align: left; margin: 10px 0; padding: 20px; min-height: 220px; }
.third-row .box .title { color: #fff; font-size: 20px; font-weight: 800; border: none; }
.third-row .box .sub-title { color: #dcdee2; font-size: 14px; padding: 10px 0 15px; }

.fourth-row .box { background: #eaeaea; text-align: left; margin: 10px 0; padding: 20px; min-height: 180px; }
.fourth-row .box .title { color: #17233d; font-size: 20px; font-weight: 800; border: none; }
.fourth-row .box .sub-title { color: #515a6e; font-size: 14px; padding: 10px 0 15px; }
.fourth-row .box .sub-title a { color: #2d8cf0; }

a.button {
  display: inline-block; padding: 0.4em 1.4em; margin: 0 0.3em; border: 0.06em solid #fff;
  border-radius: 2em; text-decoration: none; color: #fff; text-align: center;
  transition: all 0.2s; font-size: 16px; cursor: pointer;
}
a.button:hover { background: rgba(255, 255, 255, 0.12); }
a.button.dark { border-color: #2d8cf0; color: #fff; background: #2d8cf0; margin: 0; }
a.button.dark:hover { background: #2b85e4; }

.footer { background-color: #fafafa; border-top: 1px solid #eee; padding: 3rem 1.5rem; }
.footer a { color: #2d8cf0; }
</style>
