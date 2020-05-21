function average (arr) {
    return arr.reduce((p, c) => p + c, 0) / arr.length;
}

function fillDetails() {
    if (!stats) return;

    // var daysMonitoring = stats.length;
    // document.querySelector("[data-name='daysMonitoring']").innerHTML += daysMonitoring

    // var firstMonitoring = stats[0].date;
    // document.querySelector("[data-name='firstMonitoring']").innerHTML += firstMonitoring

    // var lastMonitoring = stats[stats.length-1].date;
    // document.querySelector("[data-name='lastMonitoring']").innerHTML += lastMonitoring

    var averageDelay = average(stats.map(s => s.delay));
    document.querySelector("[data-name='averageDelay']").innerHTML += (averageDelay + " minuti")

    var onTimeDays = stats.filter(s => s.delay <= 0).length;
    document.querySelector("[data-name='onTimeDays']").innerHTML += onTimeDays

    var lateDays = stats.filter(s => s.delay > 0).length;
    document.querySelector("[data-name='lateDays']").innerHTML += lateDays

    var nCancelled = stats.filter((s) => s.state == "CANCELED").length;
    document.querySelector("[data-name='nCancelled']").innerHTML += nCancelled

    var nAltered = stats.filter((s) => s.state == "MODIFIED").length;
    document.querySelector("[data-name='nAltered']").innerHTML += nAltered;
}


fillDetails();
