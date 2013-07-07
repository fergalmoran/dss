// Generated by CoffeeScript 1.6.2
(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app', 'moment', 'marionette', 'vent', 'text!/tpl/UserListItemView'], function(App, moment, Marionette, vent, Template) {
    var UserItemView, _ref;

    UserItemView = (function(_super) {
      __extends(UserItemView, _super);

      function UserItemView() {
        this.initialize = __bind(this.initialize, this);        _ref = UserItemView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      UserItemView.prototype.template = _.template(Template);

      UserItemView.prototype.tagName = "tr";

      UserItemView.prototype.events = {
        "click #follow-button": "followUser",
        "click #follow-button-login": "promptLogin"
      };

      UserItemView.prototype.templateHelpers = {
        humanise: function(date) {
          return moment(date).fromNow();
        }
      };

      UserItemView.prototype.initialize = function() {
        return this.listenTo(this.model, 'change:following', this.render);
      };

      UserItemView.prototype.followUser = function() {
        console.log("UserItemView: followUser");
        return vent.trigger("user:follow", this.model);
      };

      UserItemView.prototype.promptLogin = function() {
        return vent.trigger("app:login", this.model);
      };

      return UserItemView;

    })(Marionette.ItemView);
    return UserItemView;
  });

}).call(this);
