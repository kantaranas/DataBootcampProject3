document.querySelectorAll("#charts a").forEach(function (element) {
  element.addEventListener("click", function (event) {
    event.target.dataset.chartId;
  });
});

defaultURL = "/metadata/piechart";
d3.json(defaultURL).then(function (data) {

  function piechart(data) {

    var data = [data];
    var layout = {
      margin: {
        t: 30,
        b: 50
      }
    };
    Plotly.plot("newpiechart", data, layout, { responsive: true });
  };
  piechart(data);
});
