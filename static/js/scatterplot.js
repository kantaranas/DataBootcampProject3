// Start of Weekly Scatter Plot Function ---------------------------------

document.querySelectorAll("#charts a").forEach(function (element) {
  element.addEventListener("click", function (event) {
    event.target.dataset.chartId;
  });
});


// Plot the default route once the page loads
defaultURL = "/metadata/month/linechart/";
d3.json(defaultURL).then(function (data) {
  console.log(data);

  function linechart(data) {

    var data = data;
    var layout = {
      margin: {
        t: 30,
        b: 30
      }
    };
    Plotly.plot("scatter", data, layout, { responsive: true });
  };
  linechart(data);
});

// End of weekly scatter plot