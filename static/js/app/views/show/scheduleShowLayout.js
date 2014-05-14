// Generated by CoffeeScript 1.4.0
(function() {
  var __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  define(['app', 'vent', 'marionette', 'fullcalendar', 'views/show/scheduleShowMixListView', 'models/show/showCollection', 'models/mix/mixCollection', 'text!/tpl/ShowScheduleLayout'], function(App, vent, Marionette, fullcalendar, ScheduleShowMixList, ScheduleCollection, MixCollection, Template) {
    var ScheduleShowLayout;
    ScheduleShowLayout = (function(_super) {

      __extends(ScheduleShowLayout, _super);

      function ScheduleShowLayout() {
        return ScheduleShowLayout.__super__.constructor.apply(this, arguments);
      }

      ScheduleShowLayout.prototype.template = _.template(Template);

      ScheduleShowLayout.prototype.regions = {
        availableMixes: "#external-events"
      };

      ScheduleShowLayout.prototype.initialize = function(options) {
        var _this = this;
        this.collection = new ScheduleCollection();
        this.options = options;
        this.collection = new MixCollection();
        this.collection.fetch({
          data: options,
          success: function(collection) {
            return _this.availableMixes.show(new ScheduleShowMixList({
              collection: collection
            }));
          }
        });
      };

      ScheduleShowLayout.prototype.onShow = function() {
        var _this = this;
        this.calendar = $("#calendar").fullCalendar({
          editable: true,
          droppable: true,
          selectable: true,
          selectHelper: true,
          defaultView: "agendaDay",
          buttonText: {
            prev: "<i class=\"ace-icon fa fa-chevron-left\"></i>",
            next: "<i class=\"ace-icon fa fa-chevron-right\"></i>"
          },
          header: {
            left: "prev,next today",
            center: "title",
            right: "month,agendaWeek,agendaDay"
          },
          drop: function(date, allDay, jsEvent, ui) {
            var s;
            s = new ShowItem({
              mix: com.podnoms.settings.urlRoot + jsEvent.target.id,
              start: date,
              end: date,
              description: $(jsEvent.toElement).text().trim()
            });
            s.save(null, {
              success: function(model, response) {
                _this.collection.add(model);
                _this._renderEvent(model);
                return $(_this).remove();
              },
              error: function(model, response) {
                return utils.showError(response.responseText);
              }
            });
          },
          selectable: true,
          selectHelper: true,
          select: function(start, end, allDay) {
            calendar.fullCalendar("renderEvent", {
              title: title,
              start: start,
              end: end,
              allDay: allDay
            }, true);
            calendar.fullCalendar("unselect");
          },
          eventClick: function(calEvent, jsEvent, view) {
            var modal;
            modal = "<div class=\"modal fade\">\t\t\t  <div class=\"modal-dialog\">\t\t\t   <div class=\"modal-content\">\t\t\t\t <div class=\"modal-body\">\t\t\t\t   <button type=\"button\" class=\"close\" data-dismiss=\"modal\" style=\"margin-top:-10px;\">&times;</button>\t\t\t\t   <form class=\"no-margin\">\t\t\t\t\t  <label>Change event name &nbsp;</label>\t\t\t\t\t  <input class=\"middle\" autocomplete=\"off\" type=\"text\" value=\"" + calEvent.title + "\" />\t\t\t\t\t <button type=\"submit\" class=\"btn btn-sm btn-success\"><i class=\"ace-icon fa fa-check\"></i> Save</button>\t\t\t\t   </form>\t\t\t\t </div>\t\t\t\t <div class=\"modal-footer\">\t\t\t\t\t<button type=\"button\" class=\"btn btn-sm btn-danger\" data-action=\"delete\"><i class=\"ace-icon fa fa-trash-o\"></i> Delete Event</button>\t\t\t\t\t<button type=\"button\" class=\"btn btn-sm\" data-dismiss=\"modal\"><i class=\"ace-icon fa fa-times\"></i> Cancel</button>\t\t\t\t </div>\t\t\t  </div>\t\t\t </div>\t\t\t</div>";
            modal = $(modal).appendTo("body");
            modal.find("form").on("submit", function(ev) {
              ev.preventDefault();
              calEvent.title = $(this).find("input[type=text]").val();
              calendar.fullCalendar("updateEvent", calEvent);
              modal.modal("hide");
            });
            modal.find("button[data-action=delete]").on("click", function() {
              calendar.fullCalendar("removeEvents", function(ev) {
                return ev._id === calEvent._id;
              });
              modal.modal("hide");
            });
            modal.modal("show").on("hidden", function() {
              modal.remove();
            });
          }
        });
        return this.collection.fetch({
          data: this.options,
          success: function() {
            console.log("ScheduleView: Collection fetched");
            _this.collection.each(function(model, index, context) {
              return $("#calendar").fullCalendar("renderEvent", {
                title: model.get("description"),
                start: model.get("start"),
                end: model.get("end"),
                allDay: false,
                className: "label-important"
              });
            });
          }
        });
      };

      true;

      return ScheduleShowLayout;

    })(Marionette.Layout);
    return ScheduleShowLayout;
  });

}).call(this);
