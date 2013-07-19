// Generated by CoffeeScript 1.6.2
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app', 'toastr', 'app.lib/editableView', 'moment', 'libs/backbone/backbone.syphon', 'text!/tpl/UserEditView'], function(App, toastr, EditableView, moment, Syphon, Template) {
    var UserEditView, _ref;

    UserEditView = (function(_super) {
      __extends(UserEditView, _super);

      function UserEditView() {
        _ref = UserEditView.__super__.constructor.apply(this, arguments);
        return _ref;
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
          $("#file_upload").uploadifive({
            uploadScript: "ajax/upload_avatar_image/"
          });
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
          $("#div_avatar_image_upload", this.el).show();
          return $("#file_upload").uploadifive({
            uploadScript: "ajax/upload_avatar_image/"
          });
        } else {
          return $("#div_avatar_image_upload", this.el).hide();
        }
      };

      UserEditView.prototype.saveChanges = function() {
        var data, ref;

        data = Backbone.Syphon.serialize(this);
        this.model.set(data);
        ref = this;
        this._saveChanges({
          success: function() {
            if (ref.model.get('avatar_type') === "custom") {
              $.ajaxFileUpload({
                url: "/ajax/upload_avatar_image/",
                secureuri: false,
                fileElementId: "avatar_image",
                success: function(data, status) {
                  if (typeof data.error !== "undefined") {
                    if (data.error !== "") {
                      return alert(data.error);
                    } else {
                      return alert(data.msg);
                    }
                  } else {
                    toastr.info("Successfully updated yourself");
                    return Backbone.history.navigate("/", {
                      trigger: true
                    });
                  }
                },
                error: function(data, status, e) {
                  return alert(e);
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
