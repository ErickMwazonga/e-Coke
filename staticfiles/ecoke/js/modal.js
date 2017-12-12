$(function () {

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-brand").modal("show");
      },
      success: function (data) {
        $("#modal-brand .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#brand-table tbody").html(data.html_brand_list);
          $("#modal-brand").modal("hide");
        }
        else {
          $("#modal-brand.modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  /* Binding */
  // Create brand
  $(".js-create-brand").click(loadForm);
  $("#modal-brand").on("submit", ".js-brand-create-form", saveForm);
  // Update brand
  $("#brand-table").on("click", ".js-update-brand", loadForm);
  $("#modal-brand").on("submit", ".js-brand-update-form", saveForm);
  // Delete brand
  $("#brand-table").on("click", ".js-delete-brand", loadForm);
  $("#modal-brand").on("submit", ".js-brand-delete-form", saveForm);
});
