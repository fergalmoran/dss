define ['app', 'vent', 'utils', 'marionette', 'fullcalendar',
        'views/show/scheduleShowMixListView',
        'models/show/showCollection', 'models/show/showItem',
        'models/mix/mixCollection',
        'text!/tpl/ShowScheduleLayout'],
(App, vent, utils, Marionette, fullcalendar,
 ScheduleShowMixList,
 ShowCollection, ShowItem,
 MixCollection,
 Template)->
    class ScheduleShowLayout extends Marionette.Layout
        template: _.template(Template)
        regions:
            availableMixes: "#external-events"

        initialize: (options)->
            @collection = new ShowCollection()
            @options = options

            @mixCollection = new MixCollection()
            @mixCollection.fetch
                data: {for_show: true, order_by: 'latest'}
                success: (collection)=>
                    @availableMixes.show(new ScheduleShowMixList({collection: collection}))
            return

        onShow: =>
            @calendar = $("#calendar").fullCalendar(
                editable: true
                droppable: true
                selectable: true
                selectHelper: true
                defaultView: "agendaDay"

                buttonText:
                    prev: "<i class=\"ace-icon fa fa-chevron-left\"></i>"
                    next: "<i class=\"ace-icon fa fa-chevron-right\"></i>"

                header:
                    left: "prev,next today"
                    center: "title"
                    right: "month,agendaWeek,agendaDay"

                drop: (date, allDay, jsEvent, ui) =>
                    s = new ShowItem(
                        mix: com.podnoms.settings.urlRoot + jsEvent.target.id
                        start: date
                        end: date
                        description: $(jsEvent.toElement).text().trim()
                    )
                    s.save null,
                        success: (model, response) =>
                            @collection.add(model)
                            @_renderEvent(model)
                            $(this).remove()  # if $("#drop-remove").is(":checked")
                        error: (model, response) =>
                            utils.showError(response.responseText)
                    return

                eventClick: (calEvent, jsEvent, view) ->

                    #display a modal
                    modal = "<div class=\"modal fade\">\t\t\t  <div class=\"modal-dialog\">\t\t\t   <div class=\"modal-content\">\t\t\t\t <div class=\"modal-body\">\t\t\t\t   <button type=\"button\" class=\"close\" data-dismiss=\"modal\" style=\"margin-top:-10px;\">&times;</button>\t\t\t\t   <form class=\"no-margin\">\t\t\t\t\t  <label>Change event name &nbsp;</label>\t\t\t\t\t  <input class=\"middle\" autocomplete=\"off\" type=\"text\" value=\"" + calEvent.title + "\" />\t\t\t\t\t <button type=\"submit\" class=\"btn btn-sm btn-success\"><i class=\"ace-icon fa fa-check\"></i> Save</button>\t\t\t\t   </form>\t\t\t\t </div>\t\t\t\t <div class=\"modal-footer\">\t\t\t\t\t<button type=\"button\" class=\"btn btn-sm btn-danger\" data-action=\"delete\"><i class=\"ace-icon fa fa-trash-o\"></i> Delete Event</button>\t\t\t\t\t<button type=\"button\" class=\"btn btn-sm\" data-dismiss=\"modal\"><i class=\"ace-icon fa fa-times\"></i> Cancel</button>\t\t\t\t </div>\t\t\t  </div>\t\t\t </div>\t\t\t</div>"
                    modal = $(modal).appendTo("body")
                    modal.find("form").on "submit", (ev) ->
                        ev.preventDefault()
                        calEvent.title = $(this).find("input[type=text]").val()
                        calendar.fullCalendar "updateEvent", calEvent
                        modal.modal "hide"
                        return

                    modal.find("button[data-action=delete]").on "click", ->
                        calendar.fullCalendar "removeEvents", (ev) ->
                            ev._id is calEvent._id

                        modal.modal "hide"
                        return

                    modal.modal("show").on "hidden", ->
                        modal.remove()
                        return

                    return
            )
            @_fetchEvents()

        _fetchEvents: ->
            @collection.fetch(
                data: @options
                success: =>
                    console.log("ScheduleView: Collection fetched")
                    @collection.each (model) =>
                        @_renderEvent(model)
                    return
            )

        _renderEvent: (model) ->
            $("#calendar").fullCalendar("renderEvent", {
                title: model.get("description").substring(0, 15),
                start: model.get("start"),
                end: model.get("end"),
                allDay: false,
                className: "label-important"
            })
        true
    ScheduleShowLayout


