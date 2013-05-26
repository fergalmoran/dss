// Generated by CoffeeScript 1.3.3
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app', 'marionette', 'models/mix/mixItem', 'views/mix/mixListView', 'views/mix/mixDetailView', 'views/mix/mixEditView', 'models/user/userItem', 'views/user/userEditView'], function(App, Marionette, MixItem, MixListView, MixDetailView, MixEditView, UserItem, UserEditView) {
    var DssController;
    DssController = (function(_super) {

      __extends(DssController, _super);

      function DssController() {
        return DssController.__super__.constructor.apply(this, arguments);
      }

      DssController.prototype.home = function() {
        console.log("Controller: home");
        this.showMixList();
        return true;
      };

      DssController.prototype.showMixList = function(type, options) {
        var app;
        console.log("Controller: showMixList");
        type = type || "latest";
        app = require('app');
        app.contentRegion.show(new MixListView($.extend({
          type: type
        }, options)), 'drop');
        return true;
      };

      DssController.prototype.showMix = function(slug) {
        var app, mix;
        console.log("Controller: showMix");
        app = require('app');
        mix = new MixItem({
          id: slug
        });
        mix.fetch({
          success: function() {
            app.contentRegion.show(new MixDetailView({
              model: mix
            }));
            return true;
          }
        });
        return true;
      };

      DssController.prototype.uploadMix = function() {
        var app, mix;
        console.log("Controller: mixUpload");
        app = require('app');
        mix = new MixItem({
          title: '',
          description: '',
          mix_image: '',
          is_featured: false
        });
        app.contentRegion.show(new MixEditView({
          model: mix
        }));
        return true;
      };

      DssController.prototype.editMix = function(slug) {
        var app, mix;
        console.log("Controller: mixEdit");
        app = require('app');
        mix = new MixItem({
          id: slug
        });
        mix.fetch({
          success: function() {
            return app.contentRegion.show(new MixEditView({
              model: mix
            }));
          }
        });
        return true;
      };

      DssController.prototype.user = function(slug) {
        return this.showMixList('latest', {
          user: slug
        });
      };

      DssController.prototype.editUser = function() {
        var app, user;
        console.log("Controller: editUser");
        app = require('app');
        user = new UserItem({
          id: com.podnoms.settings.currentUser
        });
        user.fetch({
          success: function() {
            return app.contentRegion.show(new UserEditView({
              model: user
            }));
          }
        });
        return true;
      };

      return DssController;

    })(Marionette.Controller);
    return DssController;
  });

}).call(this);
