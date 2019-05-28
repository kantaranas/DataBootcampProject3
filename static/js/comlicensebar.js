
document.querySelectorAll("#charts a").forEach(function (element) {
    element.addEventListener("click", function (event) {
        event.target.dataset.chartId;
    });
});


// Plot the default route once the page loads
var defaultURL = "/comlicense";
d3.json(defaultURL).then(function (data) {
    console.log(data);

    function comlicense(data) {
        var data = [data];
        var layout = {
            margin: {
                t: 40,
                b: 40
            }
        };
        Plotly.plot("pie", data, layout, { responsive: true });
    };
    comlicense(data);
});
