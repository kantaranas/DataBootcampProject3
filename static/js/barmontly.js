document.querySelectorAll("#charts a").forEach(function (element) {
  element.addEventListener("click", function (event) {
    event.target.dataset.chartId;
  });
});


barchartURL = "/metadata/barchart/12";
d3.json(barchartURL).then(function (bardata) {
  console.log(bardata);

  function barchart(bardata) {
    var bardata = [bardata];
    var layout = {
      margin: {
        t: 30,
        b: 30
      }
    };
    Plotly.plot("bar", bardata, layout, { responsive: true });
  };
  barchart(bardata);
});

