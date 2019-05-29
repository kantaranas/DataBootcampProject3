// Start of Barchart Function -----------------------------


document.querySelectorAll("#barchart a").forEach(function (element) {
  element.addEventListener("click", function (event) {
    getDataBar(event.target.dataset.chartId);
  });
});


defaultURL = "/metadata/barchart/07";
d3.json(defaultURL).then(function (data) {
  var data = [data];
  var layout = {
    margin: {
      t: 30,
      b: 50
    }
  };
  Plotly.newPlot("bar", data, layout, { responsive: true });
});

// Load the pie chart
function getDataBar(route) {
  getDataBar(data);
};


// End of Barchart Function -----------------------------
