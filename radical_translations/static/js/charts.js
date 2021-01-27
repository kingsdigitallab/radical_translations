Vue.component('bar-chart', {
  extends: VueChartJs.Bar,
  props: ['clickHandler'],
  mixins: [VueChartJs.mixins.reactiveProp],
  mounted() {
    const self = this
    this.renderChart(this.chartData, {
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
    })
  }
})

Vue.component('bubble-chart', {
  extends: VueChartJs.Bubble,
  props: ['clickHandler'],
  mixins: [VueChartJs.mixins.reactiveProp],
  mounted() {
    const self = this
    this.renderChart(this.chartData, {
      legend: { display: true },
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              callback: function (value, index, values) {
                return self.chartData.labels[value]
              }
            }
          }
        ]
      },
      tooltips: {
        callbacks: {
          label: function (tooltipItem, data) {
            const item = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]

            return `${item.x}, ${item.title}: ${item.resources}`
          }
        }
      },
      onClick: function (evt, item) {
        if (item.length > 0) {
          const year = item[0]['_model'].label
          self.clickHandler(year, year)
        }
      }
    })
  },
  methods: {
    generateData: function () {
      var data = []
      for (var i = 0; i < 7; i++) {
        data.push({
          x: i + i,
          y: i,
          r: i
        })
      }
      return data
    }
  }
})
