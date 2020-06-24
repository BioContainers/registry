<template>
    <div class="nav-container">
        <Menu mode="horizontal" active-name="1" @on-select="menuSelect">
            <a class="logo" @click="gotoHome">
                <img src="static/logo/biocontainers-logo.png" width="40" height="40">BioContainers</a>
            <div class="menu">
                <MenuItem name="registry">
                    <Icon type="ios-search"></Icon>
                    Registry
                </MenuItem>
                <MenuItem name="documentation">
                    <Icon type="ios-information-circle-outline"></Icon>
                    Documentation
                </MenuItem>
                <MenuItem name="github">
                    <Icon type="logo-github"></Icon>
                    GitHub
                </MenuItem>
                <MenuItem name="api">
                    <Icon type="ios-barcode-outline"></Icon>
                    RestFul API
                </MenuItem>
                <MenuItem name="twitter">
                    <Icon type="logo-twitter"></Icon>
                    Twitter
                </MenuItem>
                <MenuItem name="scholar">
                    <Icon type="ios-school"></Icon>
                    Scholar
                </MenuItem>
                <Submenu  name="resources" @on-click="menuSelect">
                    <template slot="title">
                        <Icon type="ios-apps-outline"/>
                        Resources
                    </template>
                     <MenuItem name="statslink">
                             <Icon type="ios-stats"></Icon>
                             Statistics
                     </MenuItem>
                    <MenuItem name="multipackage">
                            <Icon type="ios-add-circle"></Icon>
                            Multi-tools container
                    </MenuItem>
                </Submenu>
            </div>
        </Menu>
    </div>
</template>
<script>
    export default {
        data () {
            return {

            }
        },
        methods:{
            gotoHome(){
                this.$router.push({name:'Index'});
            },
            menuSelect(name){
                switch(name){
                    case 'registry':
                        this.$router.push({name:'Registry'});
                        break;
                    case 'documentation':
                        window.open('https://biocontainers-edu.readthedocs.io/en/latest/');
                        break;
                    case 'statslink':
                        this.$router.push({name:'Mappingdata'});
                        break;
                    case 'multipackage':
                        this.$router.push({name:'Multipackage'});
                        break;
                    case 'biocontainers':
                        window.open('http://biocontainers.pro');
                        break;
                    case 'github':
                        window.open('http://github.com/Biocontainers');
                        break;
                    case 'twitter':
                        window.open('https://twitter.com/BioContainers');
                        break;
                    case 'scholar':
                        window.open('https://scholar.google.co.uk/citations?user=O6xG2-EAAAAJ');
                        break;
                    case 'api':
                        window.open('https://api.biocontainers.pro/ga4gh/trs/v2/ui/');
                        break;
                }
            } 
        }
        
    }
</script>
<style scoped>
    .nav-container{
        /*background-color: rgba(240,240,240,.95);*/
    }

    .nav-container {
        position: fixed;
        top: 0;
        width: 100%;
        z-index:1;
        min-height: 30px;
    }

    .nav-container a {
        float: left;
        display: block;
        text-align: center;
        /*padding: 14px 16px;*/
        text-decoration: none;
    }

    .navbar a {
        float: left;
        display: block;
        text-align: center;
        text-decoration: none;
        font-size: 17px;
        color: #495060;
    }

    .navbar logo{
        float: left;
        color: #495060;
        text-decoration: none;
        display: flex;
        align-items: center;
        padding-left:10px;
        font-size: 14px;
        font-weight: bold;

    }
    .logo img{
        margin-right: 10px;
        vertical-align: middle
    }
    .menu{
        float: right;
    }


</style>
<style>
    .nav-container .ivu-menu-light{
        /*background: rgba(240,240,240,.95) !important;*/
    }
</style>

