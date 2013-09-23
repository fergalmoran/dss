// Generated by CoffeeScript 1.3.3
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app', 'marionette', 'vent', 'views/chat/chatView', 'models/mix/mixItem', 'views/mix/mixListLayout', 'views/mix/mixListView', 'views/mix/mixDetailView', 'views/mix/mixEditView', 'views/user/userProfileView', 'models/user/userItem', 'views/user/userListView', 'views/user/userEditView'], function(App, Marionette, vent, ChatView, MixItem, MixListLayout, MixListView, MixDetailView, MixEditView, UserProfileView, UserItem, UserListView, UserEditView) {
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

      DssController.prototype._showMixList = function() {
        var app;
        app = require('app');
        app.contentRegion.show(new MixListLayout());
        return true;
      };

      DssController.prototype.showMixList = function(type) {
        this._showMixList();
        vent.trigger("mix:showlist", {
          order_by: type || 'latest'
        });
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

      DssController.prototype.showChat = function() {
        var app;
        console.log("Controller: showChat");
        app = require('app');
        return app.contentRegion.show(new ChatView());
      };

      DssController.prototype.showUserList = function() {
        var app;
        console.log("Controller: showUserList");
        app = require('app');
        return app.contentRegion.show(new UserListView());
      };

      DssController.prototype.showUserProfile = function(slug) {
        var app, user;
        console.log("Controller: showUserProfile");
        app = require('app');
        user = new UserItem({
          id: slug
        });
        return user.fetch({
          success: function() {
            return app.contentRegion.show(new UserProfileView({
              model: user
            }));
          },
          error: function(a, b, c) {
            return console.log("Error fetching user");
          }
        });
      };

      DssController.prototype.showUserFavourites = function(slug) {
        console.log("Controller: showUserFavourites");
        this._showMixList();
        return vent.trigger("mix:showlist", {
          order_by: 'latest',
          favourites__slug: slug
        });
      };

      DssController.prototype.showUserLikes = function(slug) {
        console.log("Controller: showUserLikes");
        this._showMixList();
        return vent.trigger("mix:showlist", {
          order_by: 'latest',
          likes__slug: slug
        });
      };

      DssController.prototype.showUserMixes = function(slug) {
        console.log("Controller: showUserMixes");
        this._showMixList();
        return vent.trigger("mix:showlist", {
          order_by: 'latest',
          user: slug
        });
      };

      DssController.prototype.showUserFollowing = function(slug) {
        var app;
        console.log("Controller: showUserFollowing");
        app = require('app');
        return app.contentRegion.show(new UserListView({
          followers__slug: slug
        }));
      };

      DssController.prototype.showUserFollowers = function(slug) {
        var app;
        console.log("Controller: showUserFollowers");
        app = require('app');
        return app.contentRegion.show(new UserListView({
          following__slug: slug
        }));
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
