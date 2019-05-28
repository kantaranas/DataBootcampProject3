// var data = [{"id":1,"address":"043 Mockingbird Place","longitude":"-86.5186","latitude":"39.1682","us_state":"Indiana"},
// {"id":2,"address":"4 Prentice Point","longitude":"-85.0707","latitude":"41.0938","us_state":"Indiana"},
// {"id":3,"address":"46 Derek Junction","longitude":"-96.7776","latitude":"32.7673","us_state":"Texas"}]
// dataURL = "metadata/table/12/belts/gender";
// dataURL = "/stats/fatal";
// var data;

var data = d3.select('body').append('div').attr('id', 'container');

d3.json("/metadata/table/12/belts/gender").then(function (error, data) {
    if (error) {
        return console.warn(error);
    }
      

   function tabulate(data, columns) {
      var table = d3.select('body').append('table');
      var thead = table.append('thead');
      var tbody = table.append('tbody');
  
      // append the header row
      thead.append('tr')
          .selectAll('th')
          .data(columns).enter()
          .append('th')
          .text(function (column) { return column; } );
  
      // create a row for each object in the data
      var rows = tbody.selectAll('tr')
          .data(data)
          .enter()
          .append('tr');
  
      // create a cell in each row for each column
      var cells = rows.selectAll('td')
          .data(function (row) {
              return columns.map(function (column)
                         { return { column: column, value: row[column] }   ;
              }    );
          })
          .enter()
          .append('td')
          .text(function (d) { return d.value; });
  
      return table;
     }
  
   // render the table(s)
   tabulate(data, ['Gender', 'Month', 'Traffic Violation', 'Traffic Violation Count', 'Yes/No']);
     
  });



// tabulate(data, ['date', 'gender', 'lat', 'lon', 'race', 'state', 'violation_type']);



// d3.json("metadata/table/12/belts/gender").then(function(error, data) {

//     if (error) {
//         return console.warn(error);
//     }

//     d3.select("body")
//             .selectAll("p")
//             .data(data)
//             .enter()
//             .append("p")
//             .text(function(d) {
//                 return d.name + ", " + d.location;
//             });
//     });

// just use this to make table http://jsfiddle.net/7WQjr/



// var tweTab = d3.select('body').append('div').attr('id', 'container');


// var mapCle = d3.json('/stats/fatal', function (err, data) {
//     if (err) { console.log(err) }
//     else {
//         console.log(data)

//         function tabulate(data, columns) {
//             var table = d3.select("#container").append("table"),
//                 thead = table.append("thead"),
//                 tbody = table.append("tbody");

//             // append the header row
//             thead.append("tr")
//                 .selectAll("th")
//                 .data(columns)
//                 .enter()
//                 .append("th")
//                 .text(function (column, i) {
//                     //    console.log(column)
//                     return column;
//                 });

//             // create a row for each object in the data
//             var rows = tbody.selectAll("tr")
//                 .data(data)
//                 .enter()
//                 .append("tr")
//                 .attr('class', function (d, i) {
//                     //  console.log(d);
//                     var bicol = (i % 2);
//                     if (bicol === 0) {
//                         return 'eve cell'
//                     }
//                     else {
//                         return 'odd cell'
//                     }
//                 })
//                 ;

//             // create a cell in each row for each column
//             var cells = rows.selectAll("td")
//                 .data(function (row, i) {
//                     //  console.log(i);
//                     return columns.map(function (column) {
//                         return { column: column, value: row[column] };
//                     });
//                 })
//                 .enter()
//                 .append("td")
//                 .html(function (d, i) {
//                     //console.log(i);
//                     //console.log(typeof(d.value))
//                     if (typeof (d.value) === 'object') {
//                         return '<p>' + d.value.name + '</p><p>@' + d.value.screen_name + '</p>'
//                     }
//                     else { return d.value }
//                     ;
//                 })

//             cells.attr('class', 'god');

//             d3.selectAll('rows')
//                 .attr('class', function (d, i) {
//                     console.log(i);
//                     return 'rower'
//                 });

//             return table;
//         };
//     }
// });