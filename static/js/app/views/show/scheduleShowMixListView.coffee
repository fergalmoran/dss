define ['app', 'vent', 'marionette', 'fullcalendar',
        'models/show/showCollection',
        'models/mix/mixCollection',
        'text!/tpl/ShowScheduleMixItem'],
(App, vent, Marionette, fullcalendar,
 ScheduleCollection, MixCollection,
 Template)->

    class ScheduleShowMixItem extends Marionette.ItemView
        template: _.template(Template)

    class ScheduleShowMixList extends Marionette.CollectionView
        itemView: ScheduleShowMixItem

        initialize: (options)->
            console.log("ScheduleShowMixList: initialize")
            true

        onShow: ->
            $("#external-events div.external-event").each ->

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
        true
    ScheduleShowMixList


