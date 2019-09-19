$(function () {

  /* Functions */
  var get_params = function() {
    var visu_type = $("#visu_type_select").val();
    if(visu_type != "Raw" && visu_type !="Table"){
        var url = $("#visu_type").attr("data-url");
        $.ajax({
            url : url + "?type=" + visu_type,
            type: 'GET',
            success: function(response){
                $("#visu_params").show();
                $("#params").html(response.html);
            }
        });
    } else {
         $("#visu_params").show();
    }
  };

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-group").modal("show");
      },
      success: function (data) {
        $("#modal-group .modal-content").html(data.html_form);
      }
    });
  };

  /* Binding */
    $("#visu_type_select").on("change", get_params);
});

