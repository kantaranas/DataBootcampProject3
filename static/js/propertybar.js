
document.querySelectorAll("#charts a").forEach(function (element) {
  element.addEventListener("click", function (event) {
    event.target.dataset.chartId;
  });
});


// Plot the default route once the page loads
var defaultURL = "/property";
d3.json(defaultURL).then(function (data) {

  function propertybar(data) {
    var data = [data];
    var layout = {
      margin: {
        t: 40,
        b: 50
      }
    };
    Plotly.plot("bar", data, layout, { responsive: true });
  };
  propertybar(data);
});
