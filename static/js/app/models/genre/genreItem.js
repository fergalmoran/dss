// Generated by CoffeeScript 1.4.0
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['backbone', 'backbone-associations'], function(Backbone) {
    var GenreItem;
    GenreItem = (function(_super) {

      __extends(GenreItem, _super);

      function GenreItem() {
        return GenreItem.__super__.constructor.apply(this, arguments);
      }

      GenreItem.prototype.urlRoot = com.podnoms.settings.urlRoot + "genres";

      return GenreItem;

    })(Backbone.Model);
    return GenreItem;
  });

}).call(this);