define ['underscore', 'backbone', 'marionette', 'vent', 'views/activity/activityListView', 'views/widgets/nowPlayingView', 'text!/tpl/SidebarView'],
(_, Backbone, Marionette, vent, ActivityListView, NowPlayingView, Template) ->

    class SidebarView extends Marionette.Layout
        template: _.template(Template)
        regions:
            topRegion: '#sidebar-top-content'
            streamRegion: '#sidebar-stream-content'


        initialize: ->
            console.log "SidebarView: initialize"
            this.listenTo(vent, 'mix:init', @mixInit)
            this.listenTo(vent, 'mix:play', @mixPlay)
            this.listenTo(vent, 'mix:pause', @mixPause)
            return

        onRender: ->
            console.log "SidebarView: onRender"
            return

        onShow: ->
            console.log "SidebarView: onShow"
            @streamRegion.show(new ActivityListView())
            $(@topRegion.el).hide()
            """
            @topRegion.show(
                new NowPlayingView(
                    model: new Backbone.Model({
                        item_url: "fdskjfhdsk", title: "Argle bargle", user_profile_url: "/", user_name: "Foo Ferra"
                    })
                ))
            """
            return

        mixInit: (model) ->
            console.log "SidebarView: mixInit"
            $(@topRegion.el).show()
            @topRegion.show(new NowPlayingView({model: model}))

    SidebarView
