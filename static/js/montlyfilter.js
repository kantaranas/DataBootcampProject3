
// Plot the default route once the page loads
var defaultURL = "/metadata/barchart/01";
var lastURL = defaultURL.split("/").pop();
d3.json(defaultURL).then(function (data) {
    var data = [data];
    var layout = {
        title: "Traffic Violations by Month-" + lastURL,
        margin: {
            t: 30,
            b: 100
        }
    };
    Plotly.newPlot("bar", data, layout, {responsive: true});
});

function piechart(data) {
    var data = [data];
    var layout = {
        margin: {
            t: 30,
            b: 100
        }
    };
    Plotly.newPlot("pie", data, layout, { responsive: true });
};


// Update the plot with new data
function updatePlotly(newdata, route) {

	var lastNewURL = route.split("/").pop();
	var update = {
		title: "Traffic Violations by Month-" + lastNewURL
	}

	Plotly.relayout("bar", update);
    Plotly.restyle("bar", "x", [newdata.x]);
    Plotly.restyle("bar", "y", [newdata.y]);

}

// Get new data whenever the dropdown selection changes
function getData(route) {

    d3.json(`/${route}`).then(function (data) {

        updatePlotly(data, route);
    });
}
