// from here:
//https://realpython.com/blog/python/django-and-ajax-form-submissions/

// Submit post on submit
$('#whenborn').on('submit', function(event){
    event.preventDefault();
    create_post();
});

$('#altdate').on('submit', function(event){
    event.preventDefault();
    next_date();
});

$('#worlddate').on('submit', function(event){
    event.preventDefault();
    world_date();
});


// AJAX for posting
function create_post() {
    $.ajax({
        url : "", // the endpoint (was create_post/)
        type : "POST", // http method
        data : { timezone : $('#id_timezone').val(),
                 day : $('#id_day').val(),
                 month : $('#id_month').val(),
                 year : $('#id_year').val(),
                 hour : $('#id_hour').val(),
                 minute : $('#id_minute').val(),
               }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            dob = json.epDob
            age = json.epAge
            ndob = json.epNextDob
            $("#epoch_dob").empty()
            $("#epoch_dob").prepend(
                "<b>Your alternative date of birth: </b>" +
                "Year " + Math.abs(dob.Year) +
                ", Month " + Math.abs(dob.Month) +
                ", Day " + Math.abs(dob.Day) +
                ", Hour " + Math.abs(dob.Hour) +
                ", Minute " + Math.abs(dob.Minute) +
                ", Epoch " + dob.Direction
                )

            $("#epoch_age").empty()
            $("#epoch_age").prepend(
                "<b>Your alternative age: </b>" +
                "Year " + Math.abs(age.Year) +
                ", Month " + Math.abs(age.Month) +
                ", Day " + Math.abs(age.Day) +
                ", Hour " + Math.abs(age.Hour) +
                ", Minute " + Math.abs(age.Minute)
                )

            $("#epoch_nextdob").empty()
            $("#epoch_nextdob").prepend(
                "<b>Next alternative birthday: </b>" +
                "Year " + Math.abs(ndob.Year) +
                ", Month " + Math.abs(ndob.Month) +
                ", Day " + Math.abs(ndob.Day) +
                ", Hour " + Math.abs(ndob.Hour) +
                ", Minute " + Math.abs(ndob.Minute) +
                ", Epoch " + ndob.Direction
                )

            $("#world_nextdob").empty()
            $("#world_nextdob").prepend(
                "<b>... and in world calendar: </b>" +
                json.wNextDob
              )
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


// AJAX for posting
function next_date() {
    $.ajax({
        url : "", // the endpoint (was create_post/)
        type : "POST", // http method
        data : { timezone : $('#id_timezone').val(),
                 day : $('#id_day').val(),
                 month : $('#id_month').val(),
                 year : $('#id_year').val(),
                 hour : $('#id_hour').val(),
                 minute : $('#id_minute').val(),
                 senderr : 'world'
               }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $("#next_date").empty()
            $("#next_date").prepend(
                "<b>Upcoming event alternative date: </b>" +
                "Year " + Math.abs(json.Year) +
                ", Month " + Math.abs(json.Month) +
                ", Day " + Math.abs(json.Day) +
                ", Hour " + Math.abs(json.Hour) +
                ", Minute " + Math.abs(json.Minute) +
                ", Epoch " + json.Direction
                )

            //console.log("json"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function world_date() {
    $.ajax({
        url : "", // the endpoint (was create_post/)
        type : "POST", // http method
        data : { timezone : $('#id_timezone').val(),
                 day : $('#id_day').val(),
                 month : $('#id_month').val(),
                 year : $('#id_year').val(),
                 hour : $('#id_hour').val(),
                 minute : $('#id_minute').val(),
                 senderr : "alt"
               }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $("#wnext_date").empty();
            $("#wnext_date").prepend( "<b>Upcoming event world date: </b>" +
                                     json.wtime );
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


// CRSF SHIT
$(function() {
    // This function gets cookie with a given name
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

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
