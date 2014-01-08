// Generated by CoffeeScript 1.4.0
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['backbone', 'models/genre/genreItem', 'app.lib/backbone.dss.model.collection'], function(Backbone, GenreItem, DssCollection) {
    var GenreCollection;
    GenreCollection = (function(_super) {

      __extends(GenreCollection, _super);

      function GenreCollection() {
        return GenreCollection.__super__.constructor.apply(this, arguments);
      }

      GenreCollection.prototype.model = GenreItem;

      return GenreCollection;

    })(DssCollection);
    return GenreCollection;
  });

}).call(this);
