// Generated by CoffeeScript 1.4.0
(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app.lib/editableView', 'vent', 'moment', 'utils', 'backbone.syphon', 'text!/tpl/MixEditView', 'models/genre/genreCollection', 'lib/jdataview', 'ace', 'dropzone', 'wizard', 'ajaxfileupload', 'jquery.fileupload', 'lib/ace/uncompressed/select2'], function(EditableView, vent, moment, utils, Syphon, Template, GenreCollection, jDataView) {
    var MixEditView;
    return MixEditView = (function(_super) {

      __extends(MixEditView, _super);

      function MixEditView() {
        this.saveChanges = __bind(this.saveChanges, this);
        return MixEditView.__super__.constructor.apply(this, arguments);
      }

      MixEditView.prototype.template = _.template(Template);

      MixEditView.prototype.events = {
        "click #login": "login",
        "change input[name='...']": "imageChanged"
      };

      MixEditView.prototype.ui = {
        image: "#mix-image",
        progress: "#mix-upload-progress",
        uploadError: '#mix-upload-error'
      };

      MixEditView.prototype.initialize = function() {
        this.guid = utils.generateGuid();
        this.uploadState = 0;
        this.detailsEntered = false;
        return this.patch = false;
      };

      MixEditView.prototype.onRender = function() {
        var wizard,
          _this = this;
        console.log("MixEditView: onRender js");
        $('.progress', this.el).hide();
        this.sendImage = false;
        if (!this.model.id) {
          $('input[name="upload-hash"]', this.el).val(this.guid);
        } else {
          $('#header-step1', this.el).remove();
          $('#step1', this.el).remove();
          $('#header-step2', this.el).addClass("active");
          $('#step2', this.el).addClass("active");
          $('.progress', this.el).hide();
          this.patch = true;
          this.uploadState = 2;
        }
        wizard = $("#fuelux-wizard", this.el).ace_wizard().on("change", function(e, info) {
          if (info.step === 1 && _this.uploadState === 0) {
            console.log("MixEditView: No mix uploaded");
            _this.ui.uploadError.fadeIn();
            $('#step1').addClass("alert-danger");
            return false;
          } else {
            return true;
          }
        }).on("finished", function(e) {
          console.log("Finished");
          return _this.saveChanges();
        });
        $("#mix-upload-form", this.el).dropzone({
          previewTemplate: '<div class=\"dz-preview dz-file-preview\">\n\
                        <div class=\"dz-details\">\n\
                            <div class=\"dz-filename\"><span data-dz-name></span></div>\n\
                            <div class=\"dz-size\" data-dz-size></div>\n\
                            <img data-dz-thumbnail />\n\
                        </div>\n\
                        <div class=\"progress progress-small progress-striped active\">\
                            <div class=\"progress-bar progress-bar-success\" data-dz-uploadprogress></div>\
                        </div>\n\
                        <div class=\"dz-success-mark\"><span></span></div>\n\
                        <div class=\"dz-error-mark\"><span></span></div>\n\
                        <div class=\"dz-error-message\"><span data-dz-errormessage></span></div>\n\
                    </div>',
          dictDefaultMessage: '<span class="bigger-150 bolder"><i class="icon-caret-right red"></i> Drop files</span> to upload\
	    			<span class="smaller-80 grey">(or click)</span> <br />\
		    		<i class="upload-icon icon-cloud-upload blue icon-3x"></i>',
          uploadprogress: function(e, progress, bytesSent) {
            var percentage;
            $('.progress', _this.el).hide();
            _this.uploadState = 1;
            percentage = Math.round(progress);
            console.log("Progressing");
            return _this.ui.progress.css("width", percentage + "%").parent().attr("data-percent", percentage + "%");
          },
          complete: function() {
            _this.uploadState = 2;
            return _this.checkRedirect();
          }
        });
        $("#genres", this.el).select2({
          placeholder: "Start typing and choose from list or create your own.",
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
          formatResult: function(genre) {
            return genre.description;
          },
          formatSelection: function(genre) {
            return "<div class='select2-user-result'>" + genre.description + "</div>";
          },
          initSelection: function(element, callback) {
            var genres, result;
            console.log("MixEditView: genres:initSelection");
            result = [];
            genres = _this.model.get("genres");
            if (genres !== undefined) {
              genres.each(function(data) {
                return result.push({
                  id: data.get("id"),
                  description: data.get("description")
                });
              });
            }
            return callback(result);
          }
        }, "createSearchChoice: (term, data) ->\n    if $(data).filter(->\n        @description.localeCompare(term) is 0\n    ).length is 0\n        id: term\n        text: term");
        return true;
      };

      MixEditView.prototype.saveChanges = function() {
        var flair,
          _this = this;
        console.log("MixEditView: saveChanges");
        this.model.set(Syphon.serialize($("#mix-details-form", this.el)[0]));
        flair = Syphon.serialize($("#mix-flair-form", this.el)[0], {
          exclude: ["...", ""]
        });
        this.model.set(flair);
        this.model.set("upload-hash", this.guid);
        this.model.set("upload-extension", $("#upload-extension", this.el).val());
        this.model.set("genres", new GenreCollection());
        $.each($("#genres", this.el).select2("data"), function(i, item) {
          "if @model.get(\"genres\") is undefined\n    @model.set(\"genres\", new GenreCollection())";
          return _this.model.get("genres").add({
            id: item.id,
            description: item.text
          });
        });
        if (!this.sendImage) {
          this.model.unset("mix_image");
        }
        this.model.unset("comments");
        this._saveChanges({
          patch: this.patch,
          success: function() {
            if (_this.sendImage) {
              $.ajaxFileUpload({
                url: "/ajax/upload_mix_image/" + _this.model.get("id") + "/",
                secureuri: false,
                fileElementId: "input[name='...']",
                success: function(data, status) {
                  if (typeof data.error !== "undefined") {
                    if (data.error !== "") {
                      return alert(data.error);
                    } else {
                      return alert(data.msg);
                    }
                  } else {
                    $("#mix-upload-wizard", _this.el).hide();
                    _this.detailsEntered = true;
                    return _this.checkRedirect();
                  }
                },
                error: function(data, status, e) {
                  return utils.showError(e);
                }
              });
            } else {
              $("#mix-upload-wizard", _this.el).hide();
              _this.detailsEntered = true;
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

      MixEditView.prototype.checkRedirect = function() {
        if (this.detailsEntered && this.uploadState === 2) {
          return Backbone.history.navigate("/mix/" + this.model.get("slug"), {
            trigger: true
          });
        }
      };

      MixEditView.prototype.login = function() {
        return vent.trigger('app:login');
      };

      MixEditView.prototype.imageChanged = function(evt) {
        return this.sendImage = true;
      };

      MixEditView;


      return MixEditView;

    })(EditableView);
  });

}).call(this);
