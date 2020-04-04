function average (arr) {
    return arr.reduce((p, c) => p + c, 0) / arr.length;
}

function displayStats() {
Chart.defaults.global.legend.display = false;

  if (!stats) return;
  var ctx = document.getElementById("statsChart").getContext("2d");

  const averageDelay = average(stats.map(s => s.delay))
  console.log(averageDelay)
  var myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: stats.map((s) => s.day),
      datasets: [
        {
          label: "Ritardo/Anticipo accumulato",
          data: stats.map((s) => s.delay),
          backgroundColor: stats.map((s) =>
            s.delay > 0 ? "rgba(255,0,0,0.7)" : "rgba(0, 255, 0, 0.7)"
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
              labelString: "Ritardo / Anticipo",
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
    },
  });
}
displayStats();
