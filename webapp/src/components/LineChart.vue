<!--<template>-->
<!--  <div>-->
<!--    <Line />-->
<!--  </div>-->
<!--</template>-->

<script>
  import { Line, mixins } from 'vue-chartjs'
  const { reactiveProp } = mixins

  export default {
    extends: Line,
    mixins: [reactiveProp],
    data () {
      return {
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
                fontColor: "#FFFFFF",
              },
              gridLines: {
                display: true
              },
              scaleLabel: {
                display: true,
                labelString: 'damage',
                fontColor: "#FFFFFF",
              }
            }],
            xAxes: [{
              ticks: {
                beginAtZero: false,
                fontColor: "#FFFFFF",
              },
              gridLines: {
                display: false
              },
              scaleLabel: {
                display: true,
                labelString: 'ticks',
                fontColor: "#FFFFFF",
              }
            }]
          },
          legend: {
            display: true,
            labels: {
              usePointStyle: false,
              fontColor: "#FFFFFF",
            }
          },
          responsive: true,
          maintainAspectRatio: false
        }
      }
    },
    props: ['chartData'],
    mounted () {
      this.renderChart(this.chartData, this.options)
    }
  }
</script>

<style scoped>

</style>