$('#contact_form').on('submit', function(e) {
    e.preventDefault();
    // do some validation

    // insert AJAX here
    $.ajax({
      url: '/feedback/',
      type: 'POST',
      
      dataType: 'json',
      data: {
        csrfmiddlewaretoken: '{{ csrf_token }}'
      },
      data: $('#contact_form').serialize(),

      beforeSend: function () {
        $('#loader').show();
      },

      success: function (data) {
        // console.log(data);
        $('#loader').hide();
        $('.ajaxResponseDisplay').append(
           '<div class="alert alert-success alert-dismissable">' +
            '<button type="button" class="close" data-dismiss="alert">' +
            '&times;</button>' + data.success + '</div>'
        );
      },

      error: function (data) {
        $('.ajaxResponseDisplay').append(
           '<div class="alert alert-warning alert-dismissable">' +
            '<button type="button" class="close" data-dismiss="alert">' +
            '&times;</button>' + data.success + '</div>'
        );
      }

    });

});
