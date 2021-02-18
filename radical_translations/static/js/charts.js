Vue.component('bar-chart', {
  extends: VueChartJs.Bar,
  props: ['clickHandler'],
  mixins: [VueChartJs.mixins.reactiveProp],
  data: function () {
    const self = this

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
            self.clickHandler(year, year)
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
    const self = this

    return {
      options: {
        legend: { display: false },
        scales: {
          yAxes: [
            {
              offset: true,
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
              const meta =
                data.datasets[tooltipItem[0].datasetIndex].data[
                  tooltipItem[0].index
                ].meta

              return `${meta.place}, ${meta.year}`
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
            self.clickHandler(meta.place, meta.year)
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
          drawTime: 'afterDatasetsDraw',
          annotations: this.getAnnotations()
        }
      }
    }
  },
  watch: {
    chartData: function () {
      this.options.annotation.annotations = this.getAnnotations()
      this.renderChart(this.chartData, this.options)
    }
  },
  mounted() {
    this.addPlugin(ChartDataLabels)
    this.renderChart(this.chartData, this.options)
  },
  methods: {
    getAnnotations: function () {
      return Object.values(this.chartData.annotations)
    }
  }
})
