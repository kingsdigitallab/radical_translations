Vue.component('bar-chart', {
  extends: VueChartJs.Bar,
  props: ['clickHandler'],
  mixins: [VueChartJs.mixins.reactiveProp],
  data: function () {
    return {
      options: {
        legend: { display: false },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              }
            }
          ]
        },
        onClick: function (evt, item) {
          if (item.length > 0) {
            const year = item[0]['_model'].label
            this.clickHandler(year, year)
          }
        }
      }
    }
  },
  mounted() {
    this.renderChart(this.chartData, this.options)
  }
})

Vue.component('events-chart', {
  extends: VueChartJs.Bubble,
  props: ['clickHandler'],
  mixins: [VueChartJs.mixins.reactiveProp],
  data: function () {
    return {
      options: {
        layout: {
          padding: {
            top: 50
          }
        },
        legend: { display: false },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                callback: function (value, index, values) {
                  return this.chart.data.labels[value]
                }
              }
            }
          ]
        },
        tooltips: {
          callbacks: {
            title: function (tooltipItem, data) {
              const item =
                data.datasets[tooltipItem[0].datasetIndex].data[
                  tooltipItem[0].index
                ]

              return `${item.meta.place}, ${item.x}`
            },
            label: function (tooltipItem, data) {
              const meta =
                data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
                  .meta

              return `${meta.n} events/${meta.resources} resources`
            }
          }
        },
        onClick: function (evt, item) {
          if (item.length > 0) {
            const meta = this.chart.data.datasets[item[0]._datasetIndex].data[
              item[0]._index
            ].meta
            console.log('event onclick')
          }
        },
        plugins: {
          datalabels: {
            align: 'top',
            color: '#212529',
            formatter: function (value, context) {
              const meta =
                context.chart.data.datasets[context.datasetIndex].data[
                  context.dataIndex
                ].meta

              return `${meta.n}/${meta.resources}`
            }
          }
        },
        annotation: {
          annotations: Object.values(this.chartData.annotations)
        }
      }
    }
  },
  mounted() {
    this.addPlugin(ChartDataLabels)
    this.renderChart(this.chartData, this.options)
  }
})
