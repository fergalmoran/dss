// Generated by CoffeeScript 1.3.3

/*
@license

----------------------------------------------

Copyright (c) 2012, Fergal Moran. All rights reserved.
Code provided under the BSD License:
*/


(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(["underscore", "marionette", "vent", "utils", "views/widgets/searchView", "views/notifications/notificationsListView", "text!/tpl/HeaderView"], function(_, Marionette, vent, utils, SearchView, NotificationsListView, Template) {
    var HeaderView;
    HeaderView = (function(_super) {
      var NowrapRegion;

      __extends(HeaderView, _super);

      function HeaderView() {
        return HeaderView.__super__.constructor.apply(this, arguments);
      }

      NowrapRegion = Marionette.Region.extend({
        open: function(view) {
          debugger;          return this.$el.html(view.$el.html());
        }
      });

      HeaderView.prototype.template = _.template(Template);

      HeaderView.prototype.events = {
        "click #header-play-pause-button": "togglePlayState",
        "click #header-login-button": "login",
        "click #header-live-button.btn-success": "playLive",
        "click #header-live-button.btn-danger": "pauseLive"
      };

      HeaderView.prototype.ui = {
        liveButton: "#header-live-button"
      };

      HeaderView.prototype.regions = {
        searchRegion: "#header-search",
        notificationsRegion: {
          selector: "#header-notifications"
        }
      };

      HeaderView.prototype.initialize = function() {
        this.render();
        this.listenTo(vent, "mix:play", this.trackPlaying);
        return this.listenTo(vent, "mix:pause", this.trackPaused);
      };

      HeaderView.prototype.onShow = function() {
        this.searchRegion.show(new SearchView());
        return this.notificationsRegion.show(new NotificationsListView());
      };

      HeaderView.prototype.login = function() {
        return vent.trigger('app:login');
      };

      HeaderView.prototype.logout = function() {
        return utils.showAlert("Success", "You are now logged out");
      };

      HeaderView.prototype.trackChanged = function(data) {
        $(this.el).find("#track-description").text(data.title);
        return $(this.el).find("#track-description").attr("href", "#" + data.item_url);
      };

      HeaderView.prototype.trackPlaying = function(data) {
        $(this.el).find("#header-play-button-icon").removeClass("icon-play");
        return $(this.el).find("#header-play-button-icon").addClass("icon-pause");
      };

      HeaderView.prototype.trackPaused = function(data) {
        $(this.el).find("#header-play-button-icon").removeClass("icon-pause");
        return $(this.el).find("#header-play-button-icon").addClass("icon-play");
      };

      HeaderView.prototype.render = function() {
        $(this.el).html(this.template());
        return this;
      };

      HeaderView.prototype.playLive = function() {
        console.log("HeaderView: playLive");
        $(this.ui.liveButton).toggleClass('btn-success', false).toggleClass('btn-danger', true);
        return vent.trigger('live:play');
      };

      HeaderView.prototype.pauseLive = function() {
        console.log("HeaderView: pauseLive");
        $(this.ui.liveButton).toggleClass('btn-success', true).toggleClass('btn-danger', false);
        return vent.trigger('live:pause');
      };

      return HeaderView;

    })(Marionette.Layout);
    return HeaderView;
  });

}).call(this);
