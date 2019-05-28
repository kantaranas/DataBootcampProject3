
document.querySelectorAll("#charts a").forEach(function (element) {
    element.addEventListener("click", function (event) {
        event.target.dataset.chartId;
    });
});


// Plot the default route once the page loads
var defaultURL = "/ppeinjury";
d3.json(defaultURL).then(function (data) {
    console.log(data);

    function ppeinjurybar(data) {
        var data = [data];
        var layout = {
            margin: {
                t: 40,
                b: 40
            }
        };
        Plotly.plot("bar", data, layout, { responsive: true });
    };
    ppeinjurybar(data);
});
