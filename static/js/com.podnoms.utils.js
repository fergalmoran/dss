/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */

if (!com) var com = {};
if (!com.podnoms) com.podnoms = {};

com.podnoms.utils = {
    // Asynchronously load templates located in separate .html files
    loadTemplate: function (views, callback) {
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
    trackPageView: function (url) {
        if (!(typeof(_gag) == "undefined"))
            _gaq.push(['_trackPageview', "/" + url]);
    },
    displayValidationErrors: function (messages) {
        for (var key in messages) {
            if (messages.hasOwnProperty(key)) {
                this.addValidationError(key, messages[key]);
            }
        }
        this.showAlert('Warning!', 'Fix validation errors and try again', 'alert-warning');
    },
    addValidationError: function (field, message) {
        var controlGroup = $('#' + field).parent().parent();
        controlGroup.addClass('error');
        $('.help-inline', controlGroup).html(message);
    },
    removeValidationError: function (field) {
        var controlGroup = $('#' + field).parent().parent();
        controlGroup.removeClass('error');
        $('.help-inline', controlGroup).html('');
    },
    modal: function (url) {
        if (url.indexOf("#") == 0) {
            $(url).modal('open');
        } else {
            $.get(url,function (data) {
                $('<div class="modal hide fade">' + data + '</div>')
                    .modal()
                    .on('hidden', function () {
                        $(this).remove();
                    }
                );
            }).success(function () {
                $('input:text:visible:first').focus();
            });
        }
    },
    showError: function (title, message) {
        this.showAlert(title, message, 'alert-error', true);
    },
    showAlert: function (title, text, klass, fade) {
        $('.alert').removeClass("alert-error alert-warning alert-success alert-info");
        $('.alert').addClass(klass);
        $('.alert').html('<strong>' + title + '</strong> ' + text);
        $('.alert').show();
        if (fade) {
            $('.alert').fadeOut(5000, function () {
            });
        }
        $('.alert').click(function () {
            this.hideAlert();
        });
    },
    showAlertModal: function (title, message) {
        $('#alert-proxy-title').text(title);
        $('#alert-proxy-message').html(message);
        $('#alert-proxy').modal();
    },
    hideAlert: function () {
        $('.alert').fadeOut('slow', function () {
        });
    },
    pad2: function (number) {
        return (number < 10 ? '0' : '') + number;
    },
    getDateAsToday: function () {
        var currentTime = new Date();
        var day = currentTime.getDate();
        var month = currentTime.getMonth() + 1;
        var year = currentTime.getFullYear();
        return (com.podnoms.utils.pad2(day) + "/" + com.podnoms.utils.pad2(month) + "/" + year);
    },
    formatJSONDate: function (jsonDate) {
        var date = new Date(parseInt(jsonDate.substr(6)));
        return date;
    },
    isEmpty: function (val) {
        return (val === undefined || val == null || val.length <= 0) ? true : false;
    },
    setHashbangHeader: function (xhr) {
        xhr.setRequestHeader('X-FB-Nonsense', 'Argle-Bargle');
    },
    generateGuid: function () {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },
    checkPlayCount: function () {
        if (document.cookie.indexOf('sessionId')) {
            $.getJSON('/ajax/session_play_count', function (data) {
                if ((data.play_count != 0) && (data.play_count % 5) == 0) {
                    com.podnoms.utils.showAlertModal(
                        "Hey There!",
                        "We've noticed you've been playing a few mixes now.<br />" +
                            "This is cool and we're happy you're enjoying the site but we would love it " +
                            "if you would consider logging in.<br />" +
                            "This will let you comment on mixes and even download them.");
                }
            });
        }
    },
    downloadURL: function downloadURL(url) {
        var iframe = document.getElementById("hiddenDownloader");
        if (iframe === null) {
            iframe = document.createElement('iframe');
            iframe.id = "hiddenDownloader";
            iframe.style.visibility = 'hidden';
            document.body.appendChild(iframe);
        }
        iframe.src = url;
    }
};

jQuery.extend({
    handleError: function (s, xhr, status, e) {
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

