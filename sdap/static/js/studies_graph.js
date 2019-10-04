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
        Plotly.relayout('graph', {
          width: 0.9 * $(window).width(),
          height: 0.9 * $(window).height()
        })
      }
    });
  };

  
  $(document).ready(function() {
    loadGraph();
  });

  $("#graph-form").on("change", "select", loadGraph);

  $("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
  });

  $(window).resize(function(e) {
    if($(window).width()<=768){
      $("#wrapper").removeClass("toggled");
    }else{
      $("#wrapper").addClass("toggled");
    }

    Plotly.relayout('graph', {
      width: 0.9 * $(window).width(),
      height: 0.9 * $(window).height()
    })
  });


});
