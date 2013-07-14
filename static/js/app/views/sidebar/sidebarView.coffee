define ['underscore', 'backbone', 'marionette', 'vent', 'views/activity/activityListView', 'views/widgets/nowPlayingView', 'text!/tpl/SidebarView'],
(_, Backbone, Marionette, vent, ActivityListView, NowPlayingView, Template) ->

    class SidebarView extends Marionette.Layout
        template: _.template(Template)
        regions:
            topRegion: '#sidebar-top-content'
            streamRegion: '#sidebar-stream-content'


        initialize: ->
            this.listenTo(vent, 'mix:init', @mixInit)
            this.listenTo(vent, 'mix:play', @mixPlay)
            this.listenTo(vent, 'mix:pause', @mixPause)
            this.listenTo(vent, 'live:started', @liveStarted)
            return

        onRender: ->
            return

        onShow: ->
            @streamRegion.show(new ActivityListView())
            $(@topRegion.el).hide()
            return

        mixInit: (model) ->
            $(@topRegion.el).show()
            @topRegion.show(new NowPlayingView({model: model}))

        liveStarted: ->
            console.log "SidebarView: livePlay"
            $.getJSON "ajax/live_now_playing/", (data) =>
                $(@topRegion.el).show()
                @topRegion.show(new NowPlayingView({
                    model: new Backbone.Model({
                        mix_image: "/static/img/radio.jpg",
                        item_url: "",
                        title: data.description,
                        user_profile_url: "",
                        user_name: data.title
                    })
                }))
            true

    SidebarView

