// Generated by CoffeeScript 1.4.0
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['marionette', 'text!/tpl/NotificationsItemView'], function(Marionette, Template) {
    var NotificationsItemView;
    return NotificationsItemView = (function(_super) {

      __extends(NotificationsItemView, _super);

      function NotificationsItemView() {
        return NotificationsItemView.__super__.constructor.apply(this, arguments);
      }

      NotificationsItemView.prototype.template = _.template(Template);

      NotificationsItemView.prototype.tagName = "li";

      return NotificationsItemView;

    })(Marionette.ItemView);
  });

}).call(this);
