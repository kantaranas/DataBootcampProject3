
document.querySelectorAll("#charts a").forEach(function (element) {
    element.addEventListener("click", function (event) {
        event.target.dataset.chartId;
    });
});


// Plot the default route once the page loads
var defaultURL = "/belts";
d3.json(defaultURL).then(function (data) {

    function beltbar(data) {
        var data = [data];
        var layout = {
            margin: {
                t: 40,
                b: 50
            }
        };
        Plotly.plot("bar", data, layout, { responsive: true });
    };
    beltbar(data);
});
