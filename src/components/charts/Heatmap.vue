<template>
    <chart class="pie-modifications" :options="option" :auto-resize="true"></chart>
</template>
<script>
var date = ['11/2017','12/2017','01/2018','02/2018','03/2018','04/2018','05/2018','06/2018','07/2018','08/2018','09/2018','10/2018','10/2018'];
var month = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'];

var results = [];




export default {
  data: function () {
    return {
        option:{
            tooltip: {
                position: 'top'
            },
            animation: false,
            grid: {
                height: '50%',
                y: '10%'
            },
            xAxis: {
                type: 'category',
                data: month,
                splitArea: {
                    show: true
                }
            },
            yAxis: {
                type: 'category',
                data: date,
                splitArea: {
                    show: true
                }
            },
            
            visualMap: {
                min: 0,
                max: 10,
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '15%'
            },
            series: [{
                name: 'Issues Created Num',
                type: 'heatmap',
                data: results,
                label: {
                    normal: {
                        show: true
                    }
                },
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        }
         /*
        option: {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                x: 'left',
                data:['直接访问','邮件营销','联盟广告','视频广告','搜索引擎']
            },
            series: [
                {
                    name:'访问来源',
                    type:'pie',
                    radius: ['50%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            show: true,
                            textStyle: {
                                fontSize: '30',
                                fontWeight: 'bold'
                            }
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },
                    data:[
                        {value:335, name:'直接访问'},
                        {value:310, name:'邮件营销'},
                        {value:234, name:'联盟广告'},
                        {value:135, name:'视频广告'},
                        {value:1548, name:'搜索引擎'}
                    ]
                }
            ]
        }*/
    }
  },

  methods:{
    
    setOptions(data){
        console.log('issues number array',data);



        for(let i in data){
            var parts = i.split('/');
            var monthtemp = parts[0];
            var datetemp = parts[1]+'/'+parts[2];
            let x;
            let y;
            let value;
            for(let j in date){
                if(date[j] == datetemp){
                    console.log('date[j]',date[j]);
                    y = j;
                    console.log('y',y);
                    break;
                }
            }
            for(let j in month){
                if(month[j] == monthtemp){
                    x = j;
                    break;
                }
            }
            value = data[i];
            let tempArray = [parseInt(x),parseInt(y),parseInt(value)];
            results.push(tempArray);
        }
        console.log('results',results);
        /*
        this.visulizationNum = data.length < this.visulizationNum ? data.length : this.visulizationNum;
        data.sort(function(a,b){
            return a.count < b.count ? 1 : -1;
        });
        var totalCount = 0;
        for(let i=0; i<data.length; i++){
            totalCount += data[i].count;
        }
        var legendName = [];
        for(let i=0; i<data.length; i++){
            legendName[i] = data[i].modificationName + ' [' + (data[i].count/totalCount*100).toFixed(1) +'%]';
            //console.log('legendName',legendName[i]);
            this.option.legend.data.push(legendName[i]);
            this.option.legend.selected[legendName[i]] = i < this.visulizationNum;
            var item = {
                value:data[i].count,
                name:legendName[i]
            }
            this.option.series[0].data.push(item);
        }*/
    }
  },
  created(){
    this.$bus.$on('show-issue', this.setOptions);
  },
  beforeCreate:function(){
    this.$bus.$off('show-issue');
  }
}
</script>

<style>
.echarts.pie-modifications {
  height: 400px !important;
  width: auto !important;
}
</style>