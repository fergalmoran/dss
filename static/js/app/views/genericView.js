// Generated by CoffeeScript 1.4.0
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['marionette'], function(Marionette) {
    var GenericView;
    return GenericView = (function(_super) {

      __extends(GenericView, _super);

      function GenericView() {
        return GenericView.__super__.constructor.apply(this, arguments);
      }

      GenericView.prototype.initialize = function(options) {
        return this.template = _.template(options.template);
      };

      true;

      return GenericView;

    })(Marionette.ItemView);
  });

}).call(this);
