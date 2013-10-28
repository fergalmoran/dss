// Generated by CoffeeScript 1.4.0
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['marionette', 'vent', 'app.lib/controller'], function(Marionette, vent, Controller) {
    var DssRouter;
    return DssRouter = (function(_super) {

      __extends(DssRouter, _super);

      function DssRouter() {
        return DssRouter.__super__.constructor.apply(this, arguments);
      }

      DssRouter.prototype.controller = new Controller;

      DssRouter.prototype.appRoutes = {
        "": "home",
        "/": "home",
        "mix/upload": "uploadMix",
        "mixes": "showMixList",
        "mixes/:type": "showMixListType",
        "mix/:slug": "showMix",
        "mix/edit/:slug": "editMix",
        "chat": "showChat",
        "random": "showRandomMix",
        "stream": "showStreamList",
        "users": "showUserList",
        "user/:slug/favourites": "showUserFavourites",
        "user/:slug/likes": "showUserLikes",
        "user/:slug/followers": "showUserFollowers",
        "user/:slug/following": "showUserFollowing",
        "user/:slug/mixes": "showUserMixes",
        "user/:slug": "showUserProfile",
        "me": "editUser"
      };

      DssRouter.prototype.initialize = function() {
        console.log("Router: initialize");
        return this.listenTo(vent, "navigate:mix", function(slug) {
          return this.navigate('mix/' + slug, true);
        });
      };

      return DssRouter;

    })(Marionette.AppRouter);
  });

}).call(this);
