define ['underscore', 'backbone', 'marionette', 'views/activity/activityListView', 'text!/tpl/SidebarView'],
(_, Backbone, Marionette, ActivityListView, Template) ->
    class SidebarView extends Marionette.Layout
        template: _.template(Template)
        className: "tabbable"
        regions:
            topRegion: '#sidebar-top-content'
            streamRegion: '#sidebar-stream-content'

        initialize: ->
            console.log "SidebarView: initialize"
            return

        onShow: ->
            console.log "SidebarView: onShow"
            #this.topRegion.show(new NowPlayingView())
            this.streamRegion.show(new ActivityListView())
            return

