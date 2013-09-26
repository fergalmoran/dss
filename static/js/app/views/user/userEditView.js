// Generated by CoffeeScript 1.3.3
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app', 'toastr', 'app.lib/editableView', 'moment', 'utils', 'backbone.syphon', 'text!/tpl/UserEditView'], function(App, toastr, EditableView, moment, utils, Syphon, Template) {
    var UserEditView;
    UserEditView = (function(_super) {

      __extends(UserEditView, _super);

      function UserEditView() {
        return UserEditView.__super__.constructor.apply(this, arguments);
      }

      UserEditView.prototype.template = _.template(Template);

      UserEditView.prototype.events = {
        "click #save-changes": "saveChanges",
        "change input[type=radio]": "selectAvatar"
      };

      UserEditView.prototype.onRender = function() {
        var avatarType;
        console.log("MixEditView: onRender");
        avatarType = this.model.get('avatar_type');
        $('#avatar_' + avatarType, this.el).attr('checked', true);
        if (avatarType === "custom") {
          $("#div_avatar_image_upload", this.el).show();
        } else {
          $("#div_avatar_image_upload", this.el).hide();
        }
        return true;
      };

      UserEditView.prototype.selectAvatar = function(evt) {
        var type;
        type = $(evt.currentTarget).val();
        this.model.set("avatar_type", type);
        if (type === "custom") {
          return $("#custom_avatar_helptext", this.el).show();
        } else {
          return $("#custom_avatar_helptext", this.el).hide();
        }
      };

      UserEditView.prototype.saveChanges = function() {
        var data, ref;
        data = Backbone.Syphon.serialize(this);
        this.model.set(data);
        ref = this;
        this._saveChanges({
          success: function() {
            var _this = this;
            if (ref.model.get('avatar_type') === "custom") {
              $.ajaxFileUpload({
                url: "ajax/upload_avatar_image/",
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
                    return Backbone.history.navigate("/", {
                      trigger: true
                    });
                  }
                },
                error: function(data, status, e) {
                  return utils.showError(e);
                }
              });
              this.uploadImage({
                el: $('#avatar_image'),
                success: function() {
                  utils.showMessage("Successfully updated yourself");
                  return Backbone.history.navigate("/", {
                    trigger: true
                  });
                }
              });
            } else {
              toastr.info("Successfully updated yourself");
              Backbone.history.navigate("/", {
                trigger: true
              });
            }
            return true;
          },
          error: function() {
            toastr.error("There was an error updating your info. Please try again later.");
            return true;
          }
        });
        return true;
      };

      false;

      return UserEditView;

    })(EditableView);
    return UserEditView;
  });

}).call(this);
