// Generated by CoffeeScript 1.6.2
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['underscore', 'backbone', 'marionette', 'vent', 'views/activity/activityListView', 'views/widgets/nowPlayingView', 'text!/tpl/SidebarView'], function(_, Backbone, Marionette, vent, ActivityListView, NowPlayingView, Template) {
    var SidebarView, _ref;

    SidebarView = (function(_super) {
      __extends(SidebarView, _super);

      function SidebarView() {
        _ref = SidebarView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      SidebarView.prototype.template = _.template(Template);

      SidebarView.prototype.regions = {
        topRegion: '#sidebar-top-content',
        streamRegion: '#sidebar-stream-content'
      };

      SidebarView.prototype.initialize = function() {
        console.log("SidebarView: initialize");
        this.listenTo(vent, 'mix:init', this.mixInit);
        this.listenTo(vent, 'mix:play', this.mixPlay);
        this.listenTo(vent, 'mix:pause', this.mixPause);
        this.listenTo(vent, 'live:started', this.liveStarted);
      };

      SidebarView.prototype.onRender = function() {
        console.log("SidebarView: onRender");
      };

      SidebarView.prototype.onShow = function() {
        console.log("SidebarView: onShow");
        this.streamRegion.show(new ActivityListView());
        $(this.topRegion.el).hide();
        "@topRegion.show(\n    new NowPlayingView(\n        model: new Backbone.Model({\n            item_url: \"fdskjfhdsk\", title: \"Argle bargle\", user_profile_url: \"/\", user_name: \"Foo Ferra\"\n        })\n    ))";
      };

      SidebarView.prototype.mixInit = function(model) {
        console.log("SidebarView: mixInit");
        $(this.topRegion.el).show();
        return this.topRegion.show(new NowPlayingView({
          model: model
        }));
      };

      SidebarView.prototype.liveStarted = function() {
        var _this = this;

        console.log("SidebarView: livePlay");
        $.getJSON("ajax/live_now_playing/", function(data) {
          $(_this.topRegion.el).show();
          return _this.topRegion.show(new NowPlayingView({
            model: new Backbone.Model({
              mix_image: "/static/img/radio.jpg",
              item_url: "",
              title: data.Description,
              user_profile_url: "",
              user_name: "Deep South Sounds Radio"
            })
          }));
        });
        return true;
      };

      return SidebarView;

    })(Marionette.Layout);
    return SidebarView;
  });

}).call(this);
