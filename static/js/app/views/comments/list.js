// Generated by CoffeeScript 1.3.3
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['marionette', 'views/comments/item', 'text!/tpl/CommentListView'], function(Marionette, CommentItemView, Template) {
    var CommentListView;
    CommentListView = (function(_super) {

      __extends(CommentListView, _super);

      function CommentListView() {
        return CommentListView.__super__.constructor.apply(this, arguments);
      }

      CommentListView.prototype.template = _.template(Template);

      CommentListView.prototype.tagName = "ul";

      CommentListView.prototype.className = "activity-listing media-list";

      CommentListView.prototype.itemView = CommentItemView;

      CommentListView.prototype.itemViewContainer = "#comment-list-container";

      CommentListView.prototype.initialize = function() {
        return console.log("CommentListView: initialize");
      };

      return CommentListView;

    })(Marionette.CompositeView);
    return CommentListView;
  });

}).call(this);
