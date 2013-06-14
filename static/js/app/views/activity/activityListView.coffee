define ['marionette', 'models/activity/activityCollection', 'views/activity/activityItemView', 'text!/tpl/ActivityListView'],
(Marionette, ActivityCollection, ActivityItemView, Template) ->
    class ActivityListView extends Marionette.CompositeView

        template: _.template(Template)
        tagName: "ul"
        className: "activity-listing media-list"
        itemView: ActivityItemView
        itemViewContainer: "#activity-list-container-ul"

        initialize: ->
            console.log "ActivityListView: initialize"
            @collection = new ActivityCollection
            @collection.fetch(
                success: =>
                    console.log "ActivityListView: Collection fetched"
                    console.log @collection
                    return
            )
            return

    ActivityListView