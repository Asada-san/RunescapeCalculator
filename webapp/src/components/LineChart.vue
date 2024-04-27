<!--<template>-->
<!--  <div>-->
<!--    <Line />-->
<!--  </div>-->
<!--</template>-->

<script>
  import { Line } from 'vue-chartjs'

  export default {
    extends: Line,
    data () {
      return {
        options: {
          // title: {
          //   display: true,
          //   text: 'Total damage over time',
          //   fontColor: "#FFFFFF",
          // },
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