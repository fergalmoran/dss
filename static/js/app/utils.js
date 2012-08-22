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
}

window.TastypieModel = Backbone.Model.extend({
    base_url:function () {
        var temp_url = Backbone.Model.prototype.url.call(this);
        return (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url + '/');
    },
    url:function () {
        return this.base_url();
    }
});

window.TastypieCollection = Backbone.Collection.extend({
    parse:function (response) {
        this.recent_meta = response.meta || {};
        return response.objects || response;
    }
});

(function () {
    var proxied = window.alert;
    window.alert = function () {
        return proxied.apply(this, arguments);
    };
})();

function generateGuid(){
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
        return v.toString(16);
    });
}