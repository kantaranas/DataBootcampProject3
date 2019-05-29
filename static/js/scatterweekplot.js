// Scatter Plot Function

document.querySelectorAll("#charts a").forEach(function (element) {
  element.addEventListener("click", function (event) {
    event.target.dataset.chartId;
  });
});


// Plot the default route once the page loads
weeklyURL = "/metadata/week/linechart/";
d3.json(weeklyURL).then(function (data) {

  function weeklychart(data) {

    var data = data;
    var layout = {
      margin: {
        t: 30,
        b: 50
      }
    };
    Plotly.plot("scatter", data, layout, { responsive: true });
  };
  weeklychart(data);
});

