// Generated by CoffeeScript 1.6.2
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app', 'moment', 'marionette', 'text!/tpl/UserListItemView'], function(App, moment, Marionette, Template) {
    var UserItemView, _ref;

    return UserItemView = (function(_super) {
      __extends(UserItemView, _super);

      function UserItemView() {
        _ref = UserItemView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      UserItemView.prototype.template = _.template(Template);

      UserItemView.prototype.tagName = "tr";

      UserItemView.prototype.templateHelpers = {
        humanise: function(date) {
          return moment(date).fromNow();
        }
      };

      return UserItemView;

    })(Marionette.ItemView);
  });

}).call(this);
