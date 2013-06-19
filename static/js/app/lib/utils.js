// Generated by CoffeeScript 1.6.2
(function() {
  define(['jquery', 'bootstrap', 'toastr'], function($, bootstrap, toastr) {
    var _this = this;

    return {
      modal: function(url) {
        if (url) {
          if (url.indexOf("#") === 0) {
            $(url).modal("open");
          } else {
            $.get(url, function(data) {
              return $(data).modal().on("hidden", function() {
                $(this).remove();
                return true;
              });
            }).success(function() {
              $("input:text:visible:first").focus();
              return true;
            });
          }
        }
        return true;
      },
      checkPlayCount: function() {
        var _this = this;

        if (document.cookie.indexOf("sessionId")) {
          $.getJSON("/ajax/session_play_count", function(data) {
            console.log("utils: got playcount");
            if ((data.play_count !== 0) && (data.play_count % com.podnoms.settings.nag_count) === 0) {
              return _this.modal("dlg/PlayCountLoginAlert");
            }
          });
        }
        return true;
      },
      showError: function(title, message) {
        return toastr.error(message, title);
      },
      showWarning: function(title, message) {
        return toastr.warning(message, title);
      },
      showAlert: function(title, message) {
        return toastr.success(message, title);
      }
    };
  });

}).call(this);
