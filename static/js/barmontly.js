document.querySelectorAll("#charts a").forEach(function (element) {
  element.addEventListener("click", function (event) {
    event.target.dataset.chartId;
  });
});


barchartURL = "/metadata/barchart/07";
d3.json(barchartURL).then(function (bardata) {

  function barchart(bardata) {
    var bardata = [bardata];
    var layout = {
      margin: {
        t: 30,
        b: 100
      }
    };
    Plotly.plot("bar", bardata, layout, { responsive: true });
  };
  barchart(bardata);
});

