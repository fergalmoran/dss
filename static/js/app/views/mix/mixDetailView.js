// Generated by CoffeeScript 1.6.2
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['marionette', 'models/mix/mixItem', 'views/mix/mixItemView', 'text!/tpl/MixDetailView'], function(Marionette, MixItem, MixItemView, Template) {
    var MixDetailView, _ref;

    MixDetailView = (function(_super) {
      __extends(MixDetailView, _super);

      function MixDetailView() {
        _ref = MixDetailView.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      MixDetailView.prototype.template = _.template(Template);

      MixDetailView.prototype.regions = {
        mix: "#mix",
        comments: "#comments"
      };

      MixDetailView.prototype.onRender = function() {
        var view;

        view = new MixItemView({
          tagName: "div",
          className: "mix-listing audio-listing-single",
          model: this.model
        });
        this.mix.show(view);
        view.renderComments();
        return true;
      };

      return MixDetailView;

    })(Marionette.Layout);
    return MixDetailView;
  });

}).call(this);
