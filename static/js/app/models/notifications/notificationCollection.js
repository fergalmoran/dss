// Generated by CoffeeScript 1.3.3
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['backbone', 'vent', 'models/notifications/notificationItem', 'app.lib/backbone.dss.model.collection'], function(Backbone, vent, NotificationItem, DssCollection) {
    var NotificationCollection;
    NotificationCollection = (function(_super) {

      __extends(NotificationCollection, _super);

      function NotificationCollection() {
        return NotificationCollection.__super__.constructor.apply(this, arguments);
      }

      NotificationCollection.prototype.model = NotificationItem;

      NotificationCollection.prototype.url = com.podnoms.settings.urlRoot + "notification/";

      NotificationCollection.prototype.limit = 5;

      NotificationCollection.prototype.initialize = function() {
        var _this = this;
        return this.listenTo(vent, "model:notification:new", function(url) {
          var item;
          console.log("NotificationCollection: notification:new");
          item = new NotificationItem();
          return item.fetch({
            url: url,
            success: function(response) {
              console.log("NotificationCollection: item fetched");
              console.log(response);
              return _this.add(response);
            }
          });
        });
      };

      NotificationCollection.prototype.comparator = function(item) {
        return -item.id;
      };

      return NotificationCollection;

    })(DssCollection);
    return NotificationCollection;
  });

}).call(this);
