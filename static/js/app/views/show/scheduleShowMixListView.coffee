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
                $(this).draggable
                    zIndex: 999
                    revert: true # will cause the event to go back to its
                    revertDuration: 0 #  original position after the drag

                return
        true
    ScheduleShowMixList


