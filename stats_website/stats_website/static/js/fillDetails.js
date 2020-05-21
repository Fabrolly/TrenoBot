function average (arr) {
    return arr.reduce((p, c) => p + c, 0) / arr.length;
}

function fillDetails(prefix, replace_stats) {
    if (replace_stats) stats = replace_stats;
    if (!prefix) prefix = "";

    if (!stats) return;

    var daysMonitoring = stats.length;
    if (document.querySelector("[data-name='" + prefix + "daysMonitoring']"))
        document.querySelector("[data-name='" + prefix + "daysMonitoring']").innerHTML += daysMonitoring

    if (stats.length > 0) {
        var firstMonitoring = stats[0].date;
        if (document.querySelector("[data-name='" + prefix + "firstMonitoring']"))
            document.querySelector("[data-name='" + prefix + "firstMonitoring']").innerHTML += firstMonitoring

        var lastMonitoring = stats[stats.length-1].date;
        if (document.querySelector("[data-name='" + prefix + "lastMonitoring']"))
            document.querySelector("[data-name='" + prefix + "lastMonitoring']").innerHTML += lastMonitoring

        var averageDelay = average(stats.map(s => s.delay));
        if (document.querySelector("[data-name='" + prefix + "averageDelay']"))
            document.querySelector("[data-name='" + prefix + "averageDelay']").innerHTML += (averageDelay.toFixed(1) + " minuti")

        var onTimeDays = stats.filter(s => s.delay <= 0).length;
        if (document.querySelector("[data-name='" + prefix + "onTimeDays']"))
            document.querySelector("[data-name='" + prefix + "onTimeDays']").innerHTML += onTimeDays

        var lateDays = stats.filter(s => s.delay > 0).length;
        if (document.querySelector("[data-name='" + prefix + "lateDays']"))
            document.querySelector("[data-name='" + prefix + "lateDays']").innerHTML += lateDays

        var nCancelled = stats.filter((s) => s.state == "CANCELED").length;
        if (document.querySelector("[data-name='" + prefix + "nCancelled']"))
            document.querySelector("[data-name='" + prefix + "nCancelled']").innerHTML += nCancelled

        var nAltered = stats.filter((s) => s.state == "MODIFIED").length;
        if (document.querySelector("[data-name='" + prefix + "nAltered']"))
            document.querySelector("[data-name='" + prefix + "nAltered']").innerHTML += nAltered;
    }
}
