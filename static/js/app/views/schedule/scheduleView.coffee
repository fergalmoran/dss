define ['app', 'vent', 'marionette', 'fullcalendar', 'text!/tpl/ScheduleView'],
(App, vent, Marionette, fullcalendar, Template)->
    class ScheduleView extends Marionette.ItemView
        template: _.template(Template)

        onShow: ->

            $("#external-events div.external-event").each ->

                # create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
                # it doesn't need to have a start or end
                eventObject =
                    title: $.trim($(this).text()) # use the element's text as the event title

                # store the Event Object in the DOM element so we can get to it later
                $(this).data "eventObject", eventObject

                # make the event draggable using jQuery UI
                $(this).draggable
                    zIndex: 999
                    revert: true # will cause the event to go back to its
                    revertDuration: 0 #  original position after the drag

                return

            date = new Date()
            d = date.getDate()
            m = date.getMonth()
            y = date.getFullYear()
            calendar = $("#calendar").fullCalendar(
                #isRTL: true,
                buttonText:
                    prev: "<i class=\"ace-icon fa fa-chevron-left\"></i>"
                    next: "<i class=\"ace-icon fa fa-chevron-right\"></i>"

                header:
                    left: "prev,next today"
                    center: "title"
                    right: "month,agendaWeek,agendaDay"

                events: [
                    {
                        title: "All Day Event"
                        start: new Date(y, m, 1)
                        className: "label-important"
                    }
                    {
                        title: "Long Event"
                        start: new Date(y, m, d - 5)
                        end: new Date(y, m, d - 2)
                        className: "label-success"
                    }
                    {
                        title: "Some Event"
                        start: new Date(y, m, d - 3, 16, 0)
                        allDay: false
                    }
                ]
                editable: true
                droppable: true # this allows things to be dropped onto the calendar !!!
                drop: (date, allDay) -> # this function is called when something is dropped

                    # retrieve the dropped element's stored Event Object
                    originalEventObject = $(this).data("eventObject")
                    $extraEventClass = $(this).attr("data-class")

                    # we need to copy it, so that multiple events don't have a reference to the same object
                    copiedEventObject = $.extend({}, originalEventObject)

                    # assign it the date that was reported
                    copiedEventObject.start = date
                    copiedEventObject.allDay = allDay
                    copiedEventObject["className"] = [$extraEventClass]  if $extraEventClass

                    # render the event on the calendar
                    # the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
                    $("#calendar").fullCalendar "renderEvent", copiedEventObject, true

                    # is the "remove after drop" checkbox checked?

                    # if so, remove the element from the "Draggable Events" list
                    $(this).remove()  if $("#drop-remove").is(":checked")
                    return

                selectable: true
                selectHelper: true
                select: (start, end, allDay) ->
                    bootbox.prompt "New Event Title:", (title) ->
                        if title isnt null
                            calendar.fullCalendar "renderEvent",
                                title: title
                                start: start
                                end: end
                                allDay: allDay
                            , true # make the event "stick"
                        return

                    calendar.fullCalendar "unselect"
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
        true

    ScheduleView


