define ['underscore', 'backbone', 'marionette', 'vent', 'views/activity/activityListView', 'views/widgets/nowPlayingView', 'text!/tpl/SidebarView'],
(_, Backbone, Marionette, vent, ActivityListView, NowPlayingView, Template) ->

    class SidebarView extends Marionette.Layout
        template: _.template(Template)
        regions:
            topRegion: '#sidebar-now-playing'
            streamRegion: '#sidebar-stream-content'


        initialize: ->
            this.listenTo(vent, 'mix:init', @mixInit)
            this.listenTo(vent, 'mix:play', @mixPlay)
            this.listenTo(vent, 'mix:pause', @mixPause)
            this.listenTo(vent, 'live:started', @liveStarted)
            this.listenTo(vent, 'live:stopped', @liveStopped)
            return

        onRender: ->
            return

        onShow: ->
            @streamRegion.show(new ActivityListView())
            $(@topRegion.el).hide()
            return

        mixInit: (model) ->
            $(@topRegion.el).show()
            @topRegion.show(new NowPlayingView({
                source: 'mix',
                model: model
            }))

        liveStarted: ->
            $(@topRegion.el).show()
            $.getJSON "/ajax/live_now_playing/", (data) =>
                vent.trigger('mix:stop')
                @topRegion.show(new NowPlayingView({
                    source: 'live'
                    model: new Backbone.Model({
                        mix_image: "/static/img/radio.jpg",
                        item_url: "",
                        title: data.description,
                        user_profile_url: "",
                        user_name: data.title
                    })
                }))
            true

        liveStopped: ->
            @topRegion.close()

    SidebarView

