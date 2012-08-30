window.utils = {
    // Asynchronously load templates located in separate .html files
    loadTemplate:function (views, callback) {

        var deferreds = [];

        $.each(views, function (index, view) {
            if (window[view]) {
                deferreds.push($.get('/tpl/' + view + '/', function (data) {
                    window[view].prototype.template = _.template(data);
                }));
            } else {
                alert(view + " not found");
            }
        });

        $.when.apply(null, deferreds).done(callback);
    },

    uploadFile:function (file, callbackSuccess) {
        var self = this;
        var data = new FormData();
        data.append('file', file);
        $.ajax({
            url:'api/upload.php',
            type:'POST',
            data:data,
            processData:false,
            cache:false,
            contentType:false
        })
            .done(function () {
                console.log(file.name + " uploaded successfully");
                callbackSuccess();
            })
            .fail(function () {
                self.showAlert('Error!', 'An error occurred while uploading ' + file.name, 'alert-error');
            });
    },

    displayValidationErrors:function (messages) {
        for (var key in messages) {
            if (messages.hasOwnProperty(key)) {
                this.addValidationError(key, messages[key]);
            }
        }
        this.showAlert('Warning!', 'Fix validation errors and try again', 'alert-warning');
    },

    addValidationError:function (field, message) {
        var controlGroup = $('#' + field).parent().parent();
        controlGroup.addClass('error');
        $('.help-inline', controlGroup).html(message);
    },

    removeValidationError:function (field) {
        var controlGroup = $('#' + field).parent().parent();
        controlGroup.removeClass('error');
        $('.help-inline', controlGroup).html('');
    },

    showAlert:function (title, text, klass, fade) {
        $('.alert').removeClass("alert-error alert-warning alert-success alert-info");
        $('.alert').addClass(klass);
        $('.alert').html('<strong>' + title + '</strong> ' + text);
        $('.alert').show();
        if (fade) {
            $('.alert').fadeOut(5000, function () {
            });
        }
        $('.alert').click(function () {
            $('.alert').fadeOut('slow', function () {
            });
        });
    },
    hideAlert:function () {
        $('.alert').hide();
    }
};
setHashbangHeader = function (xhr) {
    xhr.setRequestHeader('X-FB-Nonsense', 'Argle-Bargle');
};


jQuery.extend({
    handleError:function (s, xhr, status, e) {
        // If a local callback was specified, fire it
        if (s.error) {
            s.error.call(s.context || window, xhr, status, e);
        }

        // Fire the global callback
        if (s.global) {
            (s.context ? jQuery(s.context) : jQuery.event).trigger("ajaxError", [xhr, s, e]);
        }
    }
});
(function () {
    var proxied = window.alert;
    /*
     window.alert = function () {
     $('#alert-proxy-message').text(arguments[0]);
     $('#alert-proxy').modal();
     };
     */
})();

function generateGuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
function pad2(number) {
    return (number < 10 ? '0' : '') + number
}
function getDateAsToday() {
    var currentTime = new Date();
    var day = currentTime.getDate();
    var month = currentTime.getMonth() + 1;
    var year = currentTime.getFullYear();
    return (pad2(day) + "/" + pad2(month) + "/" + year);
}

function isEmpty(val){
    return (val === undefined || val == null || val.length <= 0) ? true : false;
}