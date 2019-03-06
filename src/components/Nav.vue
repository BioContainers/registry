<template>
    <div class="nav-container">
        <Menu mode="horizontal" active-name="1" @on-select="menuSlect">
            <a class="logo" @click="gotoHome"><img src="static/logo/biocontainers-logo.png" width="40" height="40">BioContainers</a>
            <div class="menu">
                <MenuItem name="registry">
                    <Icon type="ios-search"></Icon>
                    Registry
                </MenuItem>
                <MenuItem name="documentation">
                    <Icon type="ios-information-circle-outline"></Icon>
                    Documentation
                </MenuItem>
                <Dropdown>
                    <a href="javascript:void(0)">
                        <Icon type="ios-arrow-down"></Icon>
                        Resources
                    </a>
                    <DropdownMenu slot="list">
                        <DropdownItem name="statslink">
                             <Icon type="ios-home-outline"></Icon>
                             Statistics
                        </DropdownItem>
                        <DropdownItem name="multipackage">
                            <Icon type="ios-add-circle"></Icon>
                            Create Multi-tools container
                        </DropdownItem>
                    </DropdownMenu>
                </Dropdown>

                <!--<MenuItem name="multipackage">-->
                    <!--<Icon type="ios-add-circle"></Icon>-->
                    <!--Multi-package-->
                <!--</MenuItem>-->
                <!--<MenuItem name="statslink">-->
                   <!--<Icon type="ios-home-outline"></Icon>-->
                    <!--Statistics-->
                <!--</MenuItem>-->
                <!--<MenuItem name="biocontainers">-->
                    <!--<Icon type="ios-home-outline"></Icon>-->
                    <!--BioContainers-->
                <!--</MenuItem>-->
                <MenuItem name="github">
                    <Icon type="logo-github"></Icon>
                    GitHub
                </MenuItem>
                <MenuItem name="twitter">
                    <Icon type="logo-twitter"></Icon>
                    Twitter
                </MenuItem>
                <MenuItem name="scholar">
                    <Icon type="ios-school"></Icon>
                    Scholar
                </MenuItem>
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
            menuSlect(name){
                switch(name){
                    case 'registry':
                        this.$router.push({name:'Registry'});
                        break;
                    case 'documentation':
                        window.open('http://biocontainers-edu.biocontainers.pro');
                        break;
                  case 'statslink':
                      this.$router.push({name:'Mappingdata'});
                      break;
                  case 'multipackage':
                    this.$router.push({name:'Multipackage'});
                    //window.open('http://biocontainers.pro/multi-package-containers/');
                    //this.activeName = 'discover';
                    break;
                  case 'biocontainers':
                    //this.$router.push({ name: 'discover', params: { category: '全部'},query:{sort: "popular"}});
                    //this.activeName = 'discover';
                    window.open('http://biocontainers.pro')
                    break;
                  case 'github':
                    //this.$router.push({ name: 'discover', params: { category: '全部'},query:{sort: "popular"}});
                    //this.activeName = 'discover';
                     window.open('http://github.com/Biocontainers')
                     break;
                  case 'twitter':
                      window.open('https://twitter.com/BioContainers')
                      break;
                  case 'scholar':
                      window.open('https://scholar.google.co.uk/citations?user=O6xG2-EAAAAJ')
                      break;
                }
            } 
        }
        
    }
</script>
<style scoped>
    .nav-container{
        background-color: rgba(240,240,240,.95);
    }
    .logo{
        float: left;
        color: #495060;
        text-decoration: none;
        display: flex;
        align-items: center;
        padding-left:10px;
        font-size: 16px;
        font-weight: bold;
    }
    .logo img{
        margin-right: 10px;
    }
    .menu{
        float: right;
    }
</style>
<style>
    .nav-container .ivu-menu-light{
        background: rgba(240,240,240,.95) !important;
    }
</style>

