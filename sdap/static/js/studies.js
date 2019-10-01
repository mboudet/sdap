$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
});

$(function () {

  /* Functions */
/* In case we want to limit character numbers
  var loadTableInput = function (){
    var input = $(this);
    console.log(input.val())
    if (input.val().length > 1){
        loadTable()
    }
  }
*/
  selectRows = []

  var loadTable = function () {
    var form = $("#test-form")
    $.ajax({
      url: form.attr("data-url"),
      type: 'get',
      dataType: 'json',
      data: form.serialize(),
      success: function (data) {
        $("#table").html(data['table']);
      }
    });
  };

  var selectMe = function () {
    var row = $(this);
    var study_id = row.attr("study_id");
    var index = selectRows.indexOf(study_id);
    if(index == -1){
        row.css("background-color", "pink");
        selectRows.push(study_id);
    } else {
        row.css("background-color", "white");
        selectRows.splice(index, 1);
    }
  }

  /* Binding */
    $("#filter").on("change", "select", loadTable);
    $("#filter").on("keyup", "input", loadTable);
    $("#table").on("click", "tr", selectMe);
});
