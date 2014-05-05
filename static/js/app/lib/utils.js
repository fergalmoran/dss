// Generated by CoffeeScript 1.4.0
(function() {

  define(['jquery', 'lib/jquery.filedownload', 'bootstrap', 'toastr'], function($, filedownload, bootstrap, toastr) {
    return {
      modal: function(url) {
        if ($('#modal-header').length) {
          return;
        }
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
      secondsToHms: function(d) {
        var h, m, s;
        if (d) {
          d = Number(d);
          h = Math.floor(d / 3600);
          m = Math.floor(d % 3600 / 60);
          s = Math.floor(d % 3600 % 60);
          return (h > 0 ? h + ":" : "") + (m > 0 ? (h > 0 && m < 10 ? "0" : "") + m + ":" : "00:") + (s < 10 ? "0" : "") + s;
        } else {
          return "00:00:00";
        }
      },
      messageBox: function(url, success) {
        if (url) {
          if (url.indexOf("#") === 0) {
            $(url).modal("open");
          } else {
            $.get(url, function(data) {
              return $(data).modal('show').on("shown.bs.modal", function(e) {
                return $(this).find("#yes-no-positive").click(function() {
                  return success();
                });
              });
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
            if (data.play_count !== "0" && ((data.play_count % com.podnoms.settings.nag_count) === 0)) {
              return _this.modal("/dlg/PlayCountLoginAlert");
            }
          });
        }
        return true;
      },
      toastOptions: function() {
        return toastr.options = {
          closeButton: true,
          debug: false,
          positionClass: "toast-bottom-left",
          onclick: null,
          showDuration: "300",
          hideDuration: "1000",
          timeOut: "5000",
          extendedTimeOut: "1000",
          showEasing: "swing",
          hideEasing: "linear",
          showMethod: "fadeIn",
          hideMethod: "fadeOut"
        };
      },
      showError: function(title, message) {
        this.toastOptions();
        return toastr.error(message, title);
      },
      showWarning: function(title, message) {
        this.toastOptions();
        return toastr.warning(message, title);
      },
      showMessage: function(title, message) {
        this.toastOptions();
        return toastr.success(message, title);
      },
      showAlert: function(title, message) {
        return this.showMessage(title, message);
      },
      generateGuid: function() {
        return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(c) {
          var r, v;
          r = Math.random() * 16 | 0;
          v = (c === "x" ? r : r & 0x3 | 0x8);
          return v.toString(16);
        });
      },
      downloadURL: function(url) {
        "$.getJSON url, (data) =>\n    $.fileDownload(data.url)\n    successCallback: (url) ->\n        alert \"You just got a file download dialog or ribbon for this URL :\" + url\n        return\n\n    failCallback: (html, url) ->\n        alert \"Your file download just failed for this URL:\" + url + \"\r\n\" + \"Here was the resulting error HTML: \r\n\" + html\n        return";

        var iframe;
        iframe = document.getElementById("if_dl_misecure");
        if (iframe === null) {
          iframe = document.createElement("iframe");
          iframe.id = "if_dl_misecure";
          iframe.style.visibility = "hidden";
          document.body.appendChild(iframe);
        }
        iframe.src = url;
        return true;
      },
      isMe: function(id) {
        return id === com.podnoms.settings.currentUser;
      }
    };
  });

}).call(this);
