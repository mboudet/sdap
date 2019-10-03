$(function () {

  /* Functions */

  var loadGraph = function () {
    var div = $("#graph")
    var selected_class = $("#class_select").val();
    $.ajax({
      url: div.attr("data-url") + "&selected_class=" + selected_class,
      type: 'get',
      dataType: 'json',
      success: function (data) {
        var chart = data.chart;
        Plotly.newPlot('graph', chart.data, chart.layout, chart.config);
      }
    });
  };
  $(document).ready(function() {
    loadGraph();
  });

  $("#graph-form").on("change", "select", loadGraph);


});
