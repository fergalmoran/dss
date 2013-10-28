// Generated by CoffeeScript 1.4.0
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app', 'marionette', 'vent', 'utils', 'views/mix/mixListLayout', 'views/mix/mixListView', 'views/mix/mixDetailView', 'views/stream/streamListLayout', 'views/mix/mixEditView', 'views/user/userProfileView', 'views/user/userListView', 'views/user/userEditView', 'models/mix/mixItem', 'models/mix/mixCollection', 'models/user/userItem'], function(App, Marionette, vent, utils, MixListLayout, MixListView, MixDetailView, StreamListLayout, MixEditView, UserProfileView, UserListView, UserEditView, MixItem, MixCollection, UserItem) {
    var DssController;
    DssController = (function(_super) {

      __extends(DssController, _super);

      function DssController() {
        return DssController.__super__.constructor.apply(this, arguments);
      }

      DssController.prototype.initialize = function() {
        return this.listenTo(vent, "mix:random", this.showRandomMix);
      };

      DssController.prototype.home = function() {
        console.log("Controller: home");
        return this.showMixList();
      };

      DssController.prototype.showMixList = function(options) {
        var app;
        app = require('app');
        return app.contentRegion.show(new MixListLayout(options || {
          order_by: 'latest'
        }));
      };

      DssController.prototype.showStreamList = function() {
        return this.showMixList({
          stream: true
        });
      };

      DssController.prototype.showMixListType = function(type) {
        return this.showMixList({
          order_by: type
        });
      };

      DssController.prototype.showMix = function(slug) {
        var app, mix;
        console.log("Controller: showMix");
        app = require('app');
        mix = new MixItem({
          id: slug
        });
        return mix.fetch({
          success: function() {
            return app.contentRegion.show(new MixDetailView({
              model: mix
            }));
          }
        });
      };

      DssController.prototype.showRandomMix = function() {
        var app, mix;
        console.log("Controller: showRandomMix");
        app = require('app');
        mix = new MixItem({
          id: 'random'
        });
        mix.fetch({
          success: function() {
            return app.contentRegion.show(new MixDetailView({
              model: mix
            }));
          }
        });
        return Backbone.history.navigate("/random", {
          trigger: false
        });
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
        return this.showMixList({
          order_by: 'latest',
          favourites__slug: slug
        });
      };

      DssController.prototype.showUserLikes = function(slug) {
        console.log("Controller: showUserLikes");
        return this.showMixList({
          order_by: 'latest',
          likes__slug: slug
        });
      };

      DssController.prototype.showUserMixes = function(slug) {
        console.log("Controller: showUserMixes");
        return this.showMixList({
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
