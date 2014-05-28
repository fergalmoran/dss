@Dss.module "ActivityApp.Views", (Views, App, Backbone, Marionette) ->
    class Views.ActivityListView extends Marionette.CompositeView
        template: "activitylistview"
        tagName: "div"
        className: "widget-box"
        itemView: Views.ActivityItemView
        itemViewContainer: "#activity-container"

        initialize: ->
            @collection = new App.ActivityApp.Models.ActivityCollection
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
