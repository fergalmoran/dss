// Generated by CoffeeScript 1.3.3
(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['marionette', 'underscore', 'vent', 'utils', 'models/notifications/notificationCollection', 'views/notifications/notificationsItemView', 'text!/tpl/NotificationsListView'], function(Marionette, _, vent, utils, NotificationCollection, NotificationsItemView, Template) {
    var NotificationsListView;
    NotificationsListView = (function(_super) {

      __extends(NotificationsListView, _super);

      function NotificationsListView() {
        this.initialize = __bind(this.initialize, this);
        return NotificationsListView.__super__.constructor.apply(this, arguments);
      }

      NotificationsListView.prototype.template = _.template(Template);

      NotificationsListView.prototype.tagName = "span";

      NotificationsListView.prototype.className = "dropdown";

      NotificationsListView.prototype.itemView = NotificationsItemView;

      NotificationsListView.prototype.itemViewContainer = "#notif_list_node";

      NotificationsListView.prototype.events = {
        "click #notifications-dropdown": "showNotifications"
      };

      NotificationsListView.prototype.ui = {
        notificationSurround: "#notification-surround",
        notificationCount: "#notification-count"
      };

      NotificationsListView.prototype.initialize = function() {
        var _this = this;
        this.collection = new NotificationCollection;
        return this.collection.fetch({
          success: function() {
            _this.renderBeacon();
            return _this.collection.on({
              'add': function(model, collection) {
                _this.collection.meta.is_new += 1;
                return _this.renderBeacon(model);
              }
            });
          },
          error: function() {
            return $(_this.ui.notificationSurround).hide();
          }
        });
      };

      NotificationsListView.prototype.renderBeacon = function(model) {
        $(this.ui.notificationCount).text(this.collection.meta.is_new);
        if (this.collection.meta.is_new === 0) {
          return $(this.ui.notificationSurround).hide();
        } else {
          $(this.ui.notificationSurround).show();
          $(this.ui.notificationSurround).addClass('animate pulse');
          if (model) {
            return utils.showAlert(model.get('notification_text'));
          }
        }
      };

      NotificationsListView.prototype.showNotifications = function() {
        var _this = this;
        return $.ajax({
          url: '/ajax/mark_read/',
          type: 'post',
          success: function() {
            $(_this.ui.notificationSurround).hide();
            return _this.collection.meta.is_new = 0;
          }
        });
      };

      return NotificationsListView;

    })(Marionette.CompositeView);
    return NotificationsListView;
  });

}).call(this);