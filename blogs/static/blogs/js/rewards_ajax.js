$('#upvote').on('click', function(event){
    event.preventDefault();

    $.ajax({
        url : '/reward_blog/',
        type : 'POST',
        async: true,
        data: {
          csrfmiddlewaretoken: '{{csrf_token}}'
        },
        data : { blog_id : $('#upvote').attr("data-id") },
        dataType: 'json',

        success : function(data){
            console.log(data)
            $('#rewards_count').html(data);
        }
    });
});


// You need these methods to add the CSRF token using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
