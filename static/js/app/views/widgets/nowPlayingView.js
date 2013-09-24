// Generated by CoffeeScript 1.3.3
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['marionette', 'vent', 'text!/tpl/NowPlayingView'], function(Marionette, vent, Template) {
    var NowPlayingView;
    NowPlayingView = (function(_super) {

      __extends(NowPlayingView, _super);

      function NowPlayingView() {
        return NowPlayingView.__super__.constructor.apply(this, arguments);
      }

      NowPlayingView.prototype.template = _.template(Template);

      NowPlayingView.prototype.className = "now-playing";

      NowPlayingView.prototype.events = {
        "click #now-playing-play": "doPlay",
        "click #now-playing-pause": "doPause"
      };

      NowPlayingView.prototype.initialize = function() {
        console.log("NowPlayingView: initialize");
        this.listenTo(vent, 'mix:play', this.mixPlay);
        this.listenTo(vent, 'mix:pause', this.mixPause);
        $('#now-playing-pause', this.el).hide();
        return true;
      };

      NowPlayingView.prototype.onRender = function() {
        this.mixPlay();
        return true;
      };

      NowPlayingView.prototype.mixPause = function(model) {
        console.log("NowPlayingView: mixPause");
        $('#now-playing-play', this.el).show();
        $('#now-playing-pause', this.el).hide();
        return true;
      };

      NowPlayingView.prototype.mixPlay = function(model) {
        console.log("NowPlayingView: mixPlay");
        $('#now-playing-play', this.el).hide();
        $('#now-playing-pause', this.el).show();
        return true;
      };

      NowPlayingView.prototype.doPlay = function() {
        console.log("NowPlayingView: doPlay");
        vent.trigger('mix:play', this.model);
        return true;
      };

      NowPlayingView.prototype.doPause = function() {
        console.log("NowPlayingView: doPause");
        vent.trigger('mix:pause', this.model);
        return true;
      };

      return NowPlayingView;

    })(Marionette.ItemView);
    return NowPlayingView;
  });

}).call(this);
