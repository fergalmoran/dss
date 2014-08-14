@Dss.module "Lib", (Lib, App, Backbone, Marionette, $) ->
    class Lib.Controller extends Marionette.Controller

        initialize: ->
            @listenTo(App.vent, "mix:random", @showRandomMix)

        home: ->
            console.log "Controller: home"
            #@showDebug()
            @showMixList()

        showDebug: ->
            App.contentRegion.show(new App.PlaylistApp.Views.PlaylistLayout())

        doLogin: ->
            App.vent.trigger('app:login')

        doLogout: ->
            App.vent.trigger('app:logout')

        showSchedule: ->
            App.contentRegion.show(new ScheduleShowLayout())
            App.vent.trigger('show:schedule:show')

        showPlaylist: (slug) ->
            console.log("Showing: " + slug)
            App.contentRegion.show(new App.PlaylistApp.Views.PlaylistShowListLayout({slug: slug}))

        showMixList: (options, emptyTemplate) ->
            App.contentRegion.show(new App.MixApp.Views.MixListLayout(options or {order_by: 'latest'}, emptyTemplate))
            App.vent.trigger('mix:showlist', options or {order_by: 'latest'})

        showStreamList: () ->
            @showMixList({stream: true}, '/tpl/EmptyTemplate')

        showMixListType: (type) ->
            @showMixList({order_by: type})

        showMixListGenre: (type) ->
            @showMixList({genres__slug: type, order_by: 'latest'})

        showMix: (slug)->
            console.log "Controller: showMix"
            mix = new App.MixApp.Models.MixItem({id: slug})
            mix.fetch(
                success: ->
                    App.contentRegion.show(new App.MixApp.Views.MixDetailView({model: mix}))
            )

        showRandomMix: ->
            console.log "Controller: showRandomMix"
            mix = new App.MixApp.Models.MixItem({id: 'random'})
            mix.fetch(
                success: ->
                    App.contentRegion.show(new MixDetailView({model: mix}))
            )
            Backbone.history.navigate "/random", trigger: false

        uploadMix: ->
            console.log("Controller: mixUpload")
            mix = new App.MixApp.Models.MixItem({
                title: '',
                description: '',
                mix_image: com.podnoms.settings.staticUrl + 'img/default-track.png',
                download_allowed: true,
                is_featured: false
            });
            App.contentRegion.show(new App.MixApp.Views.MixEditView({model: mix}))
            true

        editMix: (slug) ->
            console.log("Controller: mixEdit")
            mix = new App.MixApp.Models.MixItem({id: slug})
            mix.fetch(
                success: ->
                    App.contentRegion.show(new App.MixApp.Views.MixEditView(model: mix))
            )
            true

        showChat: ->
            console.log("Controller: showChat")
            App.contentRegion.show(new ChatView())


        showUserList: ->
            console.log("Controller: showUserList")
            App.contentRegion.show(new App.UserApp.Views.UserListView())

        showUserProfile: (slug) ->
            console.log("Controller: showUserProfile")
            user = new App.UserApp.Models.UserItem({id: slug})
            user.fetch(
                success: ->
                    App.contentRegion.show(new App.UserApp.Views.UserProfileView({model: user}))
                error: (a, b, c) ->
                    console.log("Error fetching user")
            )

        showUserFavourites: (slug) ->
            console.log("Controller: showUserFavourites")
            @showMixList({order_by: 'latest', favourites__slug: slug})

        showUserLikes: (slug) ->
            console.log("Controller: showUserLikes")
            @showMixList({order_by: 'latest', likes__slug: slug})

        showUserMixes: (slug) ->
            console.log("Controller: showUserMixes")
            @showMixList({order_by: 'latest', user: slug})

        showUserFollowing: (slug) ->
            console.log("Controller: showUserFollowing")
            App.contentRegion.show(new App.UserApp.Views.UserListView({followers__slug: slug}))

        showUserFollowers: (slug) ->
            console.log("Controller: showUserFollowers")
            App.contentRegion.show(new App.UserApp.Views.UserListView({following__slug: slug}))

        editUser: ->
            console.log("Controller: editUser")
            user = new App.UserApp.Models.UserItem({id: com.podnoms.settings.currentUser })
            user.fetch(
                success: ->
                    App.contentRegion.show(new App.UserApp.Views.UserEditView(model: user))
            )
            true

    Lib.Controller
