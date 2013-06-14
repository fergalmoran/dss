// Generated by CoffeeScript 1.3.3
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['backbone', 'models/mix/mixItem', 'app.lib/backbone.dss.model.collection'], function(Backbone, MixItem, DssCollection) {
    var MixCollection;
    MixCollection = (function(_super) {

      __extends(MixCollection, _super);

      function MixCollection() {
        return MixCollection.__super__.constructor.apply(this, arguments);
      }

      MixCollection.prototype.model = MixItem;

      MixCollection.prototype.url = com.podnoms.settings.urlRoot + "mix/";

      MixCollection.prototype._parse = function(data) {
        return console.log("MixCollection: parse");
      };

      return MixCollection;

    })(DssCollection);
    return MixCollection;
  });

}).call(this);