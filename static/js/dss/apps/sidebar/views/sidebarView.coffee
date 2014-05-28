@Dss.module "SidebarApp.Views", (Views, App, Backbone, Marionette, $, _, vent) ->
    class Views.SidebarView extends Marionette.Layout
        template: "sidebarview"
        regions:
            topRegion: '#sidebar-now-playing'
            streamRegion: '#sidebar-stream-content'


        initialize: ->
            this.listenTo(App.vent, 'mix:init', @mixInit)
            this.listenTo(App.vent, 'mix:play', @mixPlay)
            this.listenTo(App.vent, 'mix:pause', @mixPause)
            this.listenTo(App.vent, 'live:started', @liveStarted)
            this.listenTo(App.vent, 'live:stopped', @liveStopped)
            return

        onRender: ->
            return

        onShow: ->
            @streamRegion.show(new App.ActivityApp.Views.ActivityListView())
            $(@topRegion.el).hide()
            return

        mixInit: (model) ->
            $(@topRegion.el).show()
            @topRegion.show(new App.NowPlayingApp.Views.NowPlayingView({
                source: 'mix',
                model: model
            }))

        liveStarted: ->
            $(@topRegion.el).show()
            $.getJSON "/ajax/live_now_playing/", (data) =>
                App.vent.trigger('mix:stop')
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

    Views.SidebarView

