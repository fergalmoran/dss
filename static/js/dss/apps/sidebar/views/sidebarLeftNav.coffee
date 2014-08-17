@Dss.module "SidebarApp.Views", (Views, App, Backbone, Marionette, $, _, vent) ->
    class Views.SidebarLeftNav extends Marionette.LayoutView
        template: "sidebarleftnav"

        regions:
            nowPlayingRegion: '#sidebar-shortcuts-now-playing'

        events:
            "click #button-mute": "muteAudio"
            "click #header-random-button": "showRandom"
            "click #header-donate-button": "donate"

        ui:
            muteButton: "#button-mute"
            muteButtonIcon: "#button-mute-icon"

        initialize: ->
            @listenTo App.vent, "mix:play", @trackPlaying
            @listenTo App.vent, "mix:pause", @trackPaused
            @listenTo App.vent, 'mix:init', @mixInit

        onRender: ->
            $('#sidebar-shortcuts-now-playing', @el).hide()

        muteAudio: ->
            if App.audioController.audioState is 0
                utils.showMessage("Hello", "Audio has been muted")
                @ui.muteButton.removeClass('btn-success')
                @ui.muteButton.addClass('btn-danger')
                @ui.muteButtonIcon.removeClass('fa-volume-up')
                @ui.muteButtonIcon.addClass('fa-volume-down')
            else
                @ui.muteButton.removeClass('btn-danger')
                @ui.muteButton.addClass('btn-success')
                @ui.muteButtonIcon.removeClass('fa-volume-down')
                @ui.muteButtonIcon.addClass('fa-volume-up')

            App.vent.trigger("audio:mute")

        showRandom: ->
            App.vent.trigger("mix:random")

        donate: ->
            App.vent.trigger('app:donate')

        mixInit: (model) ->
            $(@nowPlayingRegion.el).show()
            @nowPlayingRegion.show(new App.NowPlayingApp.Views.NowPlayingView({
                source: 'mix',
                model: model
            }))

    Views.SidebarView

