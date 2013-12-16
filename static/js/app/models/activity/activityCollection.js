// Generated by CoffeeScript 1.4.0
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['backbone', 'vent', 'models/activity/activityItem', 'app.lib/backbone.dss.model.collection'], function(Backbone, vent, ActivityItem, DssCollection) {
    var ActivityCollection;
    ActivityCollection = (function(_super) {

      __extends(ActivityCollection, _super);

      function ActivityCollection() {
        return ActivityCollection.__super__.constructor.apply(this, arguments);
      }

      ActivityCollection.prototype.model = ActivityItem;

      ActivityCollection.prototype.url = com.podnoms.settings.urlRoot + "activity/";

      ActivityCollection.prototype.initialize = function() {
        var _this = this;
        return this.listenTo(vent, "model:activity:new", function(url) {
          var item;
          console.log("ActivityCollection: activity:new");
          item = new ActivityItem();
          return item.fetch({
            url: url,
            success: function(response) {
              console.log("ActivityCollection: item fetched");
              console.log(response);
              return _this.add(response);
            }
          });
        });
      };

      ActivityCollection.prototype.comparator = function(item) {
        return -item.id;
      };

      return ActivityCollection;

    })(DssCollection);
    return ActivityCollection;
  });

}).call(this);
