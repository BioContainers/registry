<template>
    <modal name="vulnerabilities" width="90%" height="auto" scrollable={true} @before-open="beforeOpen" >
        <div class="modal-body">
            <div v-if="msg" class="alert">{{msg}}</div>
            <Table :columns="columns" :data="vulnerabilities"></Table>

        </div>
    </modal>
</template>


<script>
  export default {
    name: 'VulnerabilitiesModal',

    data: function () {
      return {
          item: '',
          msg: '',
          columns: [
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
          ]
      }
    },

    computed: {
      vulnerabilities: function () {
        return this.item
      }
    },

    methods: {
      beforeOpen (event) {
        console.log('modal input', event.params.vulnerabilities)
        this.item = event.params.vulnerabilities;
        this.msg = event.params.msg;
      }
    }
  }
</script>

<style scoped>


.modal-body {
  margin: 20px 0;
  padding: 10px;

}

.alert {
  padding: 20px;
  background-color: #ff9800; 
  color: white;
  margin-bottom: 15px;    
}


</style>

