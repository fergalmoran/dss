// Generated by CoffeeScript 1.3.3
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['marionette', 'app.lib/controller'], function(Marionette, Controller) {
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
        "mixes": "showMixList",
        "mixes/:type": "showMixList",
        "mix/:slug": "showMix",
        "mix/edit/:slug": "editMix",
        "user/:slug": "user",
        "me": "editUser"
      };

      return DssRouter;

    })(Marionette.AppRouter);
  });

}).call(this);
