// Generated by CoffeeScript 1.4.0
(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app.lib/dssView', 'utils', 'ace-editable', 'typeahead'], function(DssView, utils) {
    var EditableView;
    return EditableView = (function(_super) {

      __extends(EditableView, _super);

      function EditableView() {
        this.setupImageEditable = __bind(this.setupImageEditable, this);
        return EditableView.__super__.constructor.apply(this, arguments);
      }

      EditableView.prototype.events = {
        "change input": "changed",
        "change textarea": "changed"
      };

      EditableView.prototype.changeSelect = function(evt) {
        var changed, obj, objInst, value;
        changed = evt.currentTarget;
        if (id) {
          value = $(evt.currentTarget).val();
          obj = "{\"" + changed.id + "\":\"" + value.replace(/\n/g, "<br />") + "\"}";
          objInst = JSON.parse(obj);
          return this.model.set(objInst);
        }
      };

      EditableView.prototype.changed = function(evt) {
        var changed, obj, objInst, value;
        return;
        changed = evt.currentTarget;
        if (changed.id) {
          value = void 0;
          obj = void 0;
          if ($(changed).is(":checkbox")) {
            value = $(changed).is(":checked");
            obj = "{\"" + changed.id + "\":" + value + "}";
          } else {
            value = $(changed).val();
            obj = "{\"" + changed.id + "\":\"" + value.replace(/\n/g, "<br />") + "\"}";
          }
          objInst = JSON.parse(obj);
          return this.model.set(objInst);
        }
      };

      EditableView.prototype._saveChanges = function() {
        var args, error, _results;
        args = arguments;
        if (!this.model.isValid()) {
          if (this.model.errors) {
            _results = [];
            for (error in this.model.errors) {
              $("#group-" + error, this.el).addClass("error");
              _results.push($("#error-" + error, this.el).text(this.model.errors[error]));
            }
            return _results;
          }
        } else {
          return this.model.save(null, {
            patch: args[0].patch,
            success: args[0].success,
            error: args[0].error
          });
        }
      };

      EditableView.prototype.setupImageEditable = function(options) {
        var _this = this;
        $.fn.editable.defaults.mode = 'inline';
        try {
          if (/msie\s*(8|7|6)/.test(navigator.userAgent.toLowerCase())) {
            Image.prototype.appendChild = function(el) {
              return true;
            };
          }
          return options.el.editable({
            type: "image",
            name: options.el.attr('id'),
            value: null,
            showbuttons: options.showbuttons === void 0 ? true : options.showbuttons,
            image: {
              btn_choose: options.chooseMessage ? options.chooseMessage : "Change Avatar",
              droppable: true,
              name: options.el.attr('id'),
              max_size: 2621440,
              on_error: function(code) {
                if (code === 1) {
                  return utils.showError("File is not an image!", "Please choose a jpg|gif|png image!");
                } else if (code === 2) {
                  return utils.showError("File too big!", "Image size should not exceed 2.5Mb!");
                } else {

                }
              }
            },
            url: function(params) {
              return _this.uploadImage({
                el: options.el,
                url: options.url,
                success: function(data) {
                  console.log("Image updated: " + data.url);
                  options.el.attr("src", data.url);
                  return utils.showMessage("Avatar succesfully updated");
                }
              });
            }
          });
        } catch (e) {
          return console.log(e);
        }
      };

      EditableView.prototype.uploadImage = function(options) {
        var $form, deferred, fd, file_input, files, iframe_id;
        $form = options.el.next().find(".editableform:eq(0)");
        file_input = $form.find("input[type=file]:eq(0)");
        if (!("FormData" in window)) {
          deferred = new $.Deferred;
          iframe_id = "temporary-iframe-" + (new Date()).getTime() + "-" + (parseInt(Math.random() * 1000));
          $form.after("<iframe id=\"" + iframe_id + "\" name=\"" + iframe_id + "\" frameborder=\"0\" width=\"0\" height=\"0\" src=\"about:blank\" style=\"position:absolute;z-index:-1;\"></iframe>");
          $form.append("<input type=\"hidden\" name=\"temporary-iframe-id\" value=\"" + iframe_id + "\" />");
          $form.next().data("deferrer", deferred);
          $form.attr({
            method: "POST",
            enctype: "multipart/form-data",
            target: iframe_id,
            action: options.url
          });
          $form.get(0).submit();
          setTimeout((function() {
            var iframe;
            iframe = document.getElementById(iframe_id);
            if (iframe != null) {
              iframe.src = "about:blank";
              $(iframe).remove();
              return deferred.reject({
                status: "fail",
                message: "Timeout!"
              });
            }
          }), 60000);
        } else {
          fd = null;
          try {
            fd = new FormData($form.get(0));
          } catch (e) {
            fd = new FormData();
            $.each($form.serializeArray(), function(index, item) {
              return fd.append(item.name, item.value);
            });
            $form.find("input[type=file]").each(function() {
              if (this.files.length > 0) {
                return fd.append(this.getAttribute("name"), this.files[0]);
              }
            });
          }
          if (file_input.data("ace_input_method") === "drop") {
            files = file_input.data("ace_input_files");
            if (files && files.length > 0) {
              fd.append(file_input.attr("name"), files[0]);
            }
          }
          deferred = $.ajax({
            url: options.url,
            type: "POST",
            processData: false,
            contentType: false,
            dataType: "json",
            data: fd,
            xhr: function() {
              var req;
              req = $.ajaxSettings.xhr();
              return req;
            },
            beforeSend: function() {
              return {
                success: function() {}
              };
            }
          });
        }
        deferred.done(function(res) {
          if (res.status === "OK") {
            return options.success(res);
          } else {
            return utils.showError(res.message);
          }
        }).fail(function(res) {
          return utils.showError("Failure");
        });
        return deferred.promise();
      };

      return EditableView;

    })(DssView);
  });

}).call(this);
