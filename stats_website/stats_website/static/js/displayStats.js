function average (arr) {
    return arr.reduce((p, c) => p + c, 0) / arr.length;
}

function displayStats() {
  Chart.defaults.global.legend.display = false;

  if (!stats) return;
  var ctx = document.getElementById("statsChart").getContext("2d");

  const averageDelay = average(stats.filter(s => s.delay).map(s => s.delay))
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: stats.map((s) => s.date),
      datasets: [
        {
          label: "Ritardo/Anticipo (min)",
          data: stats.map((s) => s.delay),
          backgroundColor: stats.map((s) => {
            if (s.state == "MODIFIED") return "rgba(255,128,0,0.7)"
            if (s.state == "CANCELED") return "rgba(0,0,0,0.7)"
            return s.delay > 0 ? "rgba(255,0,0,0.7)" : "rgba(0, 255, 0, 0.7)"
          }
          ),
          fill: false,
        },
        {
          label: "Ritardo Medio",
          data: stats.map((s) => averageDelay),
          fill: false,
          type: "line"
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      title: {
        display: true,
        text: "Ritardo Giornaliero (minuti)",
      },
      scales: {
        yAxes: [
          {
            ticks: {
              display: true,
              beginAtZero: true,
            },
            scaleLabel: {
              display: true,
              labelString: "Ritardo / Anticipo (min)",
            },
          },
        ],
        xAxes: [
          {
            ticks: {
              display: true,
              beginAtZero: true,
            },
            scaleLabel: {
              display: true,
              labelString: "Giorno",
            },
          },
        ],
      },
    }
  });
  document.getElementById('chart-legend').innerHTML = generateLegend();
}

function generateLegend(chart) {
  var text = [];
  text.push('<span class="mr-2"><span class="px-2" style="background-color:rgba(255,0,0,0.7)"></span>&nbsp;In ritardo</span>');
  text.push('<span class="mr-2"><span class="px-2" style="background-color:rgba(0,255,0,0.7)"></span>&nbsp;In anticipo</span>');
  text.push('<span class="mr-2"><span class="px-2" style="background-color:rgba(255,128,0,0.7)"></span>&nbsp;Modificato</span>');
  text.push('<span class="mr-2"><span class="px-2" style="background-color:rgba(0,0,0,0.7)"></span>&nbsp;Cancellato</span>');
  return text.join("");
}

displayStats();
