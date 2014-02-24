// Generated by CoffeeScript 1.4.0
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['models/user/userCollection', 'app.lib/backbone.dss.model'], function(UserCollection, DssModel) {
    var UserItem;
    UserItem = (function(_super) {

      __extends(UserItem, _super);

      function UserItem() {
        return UserItem.__super__.constructor.apply(this, arguments);
      }

      UserItem.prototype.urlRoot = com.podnoms.settings.urlRoot + "user/";

      return UserItem;

    })(DssModel);
    return UserItem;
  });

}).call(this);
