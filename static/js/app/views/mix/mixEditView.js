// Generated by CoffeeScript 1.6.2
(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app.lib/editableView', 'moment', 'utils', 'libs/backbone/backbone.syphon', 'text!/tpl/MixEditView', 'jquery.form', 'jquery.fileupload', 'jquery.fileupload-process', 'jquery.fileupload-audio', 'jquery.iframe-transport', 'jquery.ui.widget', 'jquery.fileupload-ui', 'select2', 'libs/ajaxfileupload', 'bootstrap-fileupload'], function(EditableView, moment, utils, Syphon, Template) {
    var MixEditView, _ref;

    return MixEditView = (function(_super) {
      __extends(MixEditView, _super);

      function MixEditView() {
        this.saveChanges = __bind(this.saveChanges, this);        _ref = MixEditView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      MixEditView.prototype.template = _.template(Template);

      MixEditView.prototype.events = {
        "click #save-changes": "saveChanges",
        "change #mix_image": "imageChanged"
      };

      MixEditView.prototype.checkRedirect = function() {
        if (this.state === 2) {
          return Backbone.history.navigate("/mix/" + this.model.get("slug"), {
            trigger: true
          });
        }
      };

      MixEditView.prototype.initialize = function() {
        this.guid = utils.generateGuid();
        return this.state = 0;
      };

      MixEditView.prototype.onDomRefresh = function() {
        var _this = this;

        return $("#fileupload", this.el).fileupload({
          downloadTemplateId: void 0,
          url: "/_upload/",
          start: function() {
            return $("#mix-details", this.el).show();
          },
          done: function() {
            _this.state++;
            $("#div-upload-mix", _this.el).hide();
            return _this.checkRedirect();
          }
        });
      };

      MixEditView.prototype.onRender = function() {
        var parent;

        console.log("MixEditView: onRender");
        this.sendImage = false;
        parent = this;
        if (!this.model.id) {
          $("#mix-details", this.el).hide();
          $("#upload-hash", this.el).val(this.guid);
        } else {
          $("#div-upload-mix", this.el).hide();
          this.state = 1;
        }
        $("#mix-imageupload", this.el).jas_fileupload({
          uploadtype: "image"
        });
        $("#image-form-proxy", this.el).ajaxForm({
          beforeSubmit: function() {
            return $("#results").html("Submitting...");
          },
          success: function(data) {
            var $out;

            $out = $("#results");
            $out.html("Your results:");
            return $out.append("<div><pre>" + data + "</pre></div>");
          }
        });
        $("#genres", this.el).select2({
          placeholder: "Start typing and choose or press enter",
          minimumInputLength: 1,
          multiple: true,
          ajax: {
            url: "/ajax/lookup/genre/",
            dataType: "json",
            data: function(term, page) {
              return {
                q: term
              };
            },
            results: function(data, page) {
              return {
                results: data
              };
            }
          },
          initSelection: function(element, callback) {
            var genres, result;

            result = [];
            genres = parent.model.get("genre-list");
            if (genres !== undefined) {
              $.each(genres, function(data) {
                return result.push({
                  id: this.id,
                  text: this.text
                });
              });
            }
            return callback(result);
          },
          createSearchChoice: function(term, data) {
            if ($(data).filter(function() {
              return this.text.localeCompare(term) === 0;
            }).length === 0) {
              return {
                id: term,
                text: term
              };
            }
          }
        });
        return this;
      };

      MixEditView.prototype.saveChanges = function() {
        var data,
          _this = this;

        console.log("MixEditView: saveChanges");
        data = Syphon.serialize($("#mix-details-form", this.el)[0]);
        this.model.set(data);
        this.model.set("upload-hash", this.guid);
        this.model.set("upload-extension", $("#upload-extension", this.el).val());
        this.model.set("genre-list", $("#genres", this.el).select2("data"));
        if (!this.sendImage) {
          this.model.set("mix_image", "DONOTSEND");
        }
        this._saveChanges({
          success: function() {
            if (_this.sendImage) {
              $.ajaxFileUpload({
                url: "/ajax/upload_image/" + _this.model.get("id") + "/",
                secureuri: false,
                fileElementId: "mix_image",
                success: function(data, status) {
                  if (typeof data.error !== "undefined") {
                    if (data.error !== "") {
                      return alert(data.error);
                    } else {
                      return alert(data.msg);
                    }
                  } else {
                    $("#mix-details", _this.el).hide();
                    _this.state++;
                    return _this.checkRedirect();
                  }
                },
                error: function(data, status, e) {
                  return alert(e);
                }
              });
            } else {
              $("#mix-details", _this.el).hide();
              _this.state++;
              _this.checkRedirect();
            }
            return true;
          },
          error: function(model, response) {
            return utils.showError("Error", "Something went wrong<br />Nerd stuff is: " + response);
          }
        });
        return false;
      };

      MixEditView.prototype.imageChanged = function(evt) {
        this.sendImage = true;
        return true;
      };

      MixEditView;

      return MixEditView;

    })(EditableView);
  });

}).call(this);
