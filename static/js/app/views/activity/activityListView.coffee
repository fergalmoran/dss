define ['marionette', 'models/activity/activityCollection', 'views/activity/activityItemView',
        'text!/tpl/ActivityListView'],
(Marionette, ActivityCollection, ActivityItemView, Template) ->
    class ActivityListView extends Marionette.CompositeView

        template: _.template(Template)
        tagName: "ul"
        className: "activity-listing media-list"
        itemView: ActivityItemView
        itemViewContainer: "#activity-list-container-ul"

        initialize: ->
            @collection = new ActivityCollection
            @collection.fetch()

        #kinda primordial (but working) support for sorted collection view
        #based on https://github.com/marionettejs/backbone.marionette/wiki/Adding-support-for-sorted-collections
        appendHtml: (collectionView, itemView, index) ->
            childrenContainer = (if collectionView.itemViewContainer then collectionView.$(collectionView.itemViewContainer) else collectionView.$el)
            children = childrenContainer.children()
            if children.size() <= index
                childrenContainer.append itemView.el
            else
                childrenContainer.children().eq(index).before itemView.el

    ActivityListView
