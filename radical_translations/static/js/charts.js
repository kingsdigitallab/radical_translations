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

Vue.component('scatter-chart', {
  extends: VueChartJs.Bubble,
  props: ['clickHandler'],
  mixins: [VueChartJs.mixins.reactiveProp],
  mounted() {
    const self = this
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    this.renderChart(
      {
        datasets: [
          {
            label: 'My First dataset',
            backgroundColor: 'red',
            data: this.generateData()
          },
          {
            label: 'My Second dataset',
            backgroundColor: 'blue',
            data: this.generateData()
          }
        ]
      },
      {
        legend: { display: true },
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                callback: function (value, index, values) {
                  return labels[value]
                }
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
    )
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
