define ['app', 'marionette', 'vent', 'utils',
        'views/mix/mixListLayout', 'views/mix/mixListView', 'views/mix/mixDetailView',
        'views/schedule/scheduleView',
        'views/mix/mixEditView', 'views/user/userProfileView', 'views/user/userListView', 'views/user/userEditView',
        'models/mix/mixCollection', 'models/mix/mixItem', 'models/user/userItem'],
(App, Marionette, vent, utils,
 MixListLayout, MixListView, MixDetailView,
 ScheduleView,
 MixEditView, UserProfileView, UserListView, UserEditView,
 MixCollection, MixItem, UserItem)->
    class DssController extends Marionette.Controller

        initialize: ->
            @listenTo(vent, "mix:random", @showRandomMix)

        home: ->
            console.log "Controller: home"
            @showMixList()

        doLogin: ->
            vent.trigger('app:login')

        showSchedule: ->
            app = require('app')
            app.contentRegion.show(new ScheduleView())
            vent.trigger('schedule:show')

        showMixList: (options, emptyTemplate) ->
            app = require('app')
            app.contentRegion.show(new MixListLayout(options or {order_by: 'latest'}, emptyTemplate))
            vent.trigger('mix:showlist', options or {order_by: 'latest'})

        showStreamList: () ->
            @showMixList({stream: true}, '/tpl/EmptyTemplate')

        showMixListType: (type) ->
            @showMixList({order_by: type})

        showMixListGenre: (type) ->
            @showMixList({genres__slug: type, order_by: 'latest'})

        showMix: (slug)->
            console.log "Controller: showMix"
            app = require('app')
            mix = new MixItem({id: slug})
            mix.fetch(
                success: ->
                    app.contentRegion.show(new MixDetailView({model: mix}))
            )

        showRandomMix: ->
            console.log "Controller: showRandomMix"
            app = require('app')
            mix = new MixItem({id: 'random'})
            mix.fetch(
                success: ->
                    app.contentRegion.show(new MixDetailView({model: mix}))
            )
            Backbone.history.navigate "/random", trigger: false

        uploadMix: ->
            console.log("Controller: mixUpload")
            app = require('app')
            mix = new MixItem({
                title: '',
                description: '',
                mix_image: com.podnoms.settings.staticUrl + 'img/default-track.png',
                download_allowed: true,
                is_featured: false
            });
            app.contentRegion.show(new MixEditView({model: mix}))
            true

        editMix: (slug) ->
            console.log("Controller: mixEdit")
            app = require('app')
            mix = new MixItem({id: slug})
            mix.fetch(
                success: ->
                    app.contentRegion.show(new MixEditView(model: mix))
            )
            true

        showChat: ->
            console.log("Controller: showChat")
            app = require('app')
            app.contentRegion.show(new ChatView())


        showUserList: ->
            console.log("Controller: showUserList")
            app = require('app')
            app.contentRegion.show(new UserListView())

        showUserProfile: (slug) ->
            console.log("Controller: showUserProfile")
            app = require('app')
            user = new UserItem({id: slug})
            user.fetch(
                success: ->
                    app.contentRegion.show(new UserProfileView({model: user}))
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
            app = require('app')
            app.contentRegion.show(new UserListView({followers__slug: slug}))

        showUserFollowers: (slug) ->
            console.log("Controller: showUserFollowers")
            app = require('app')
            app.contentRegion.show(new UserListView({following__slug: slug}))

        editUser: ->
            console.log("Controller: editUser")
            app = require('app')
            user = new UserItem({id: com.podnoms.settings.currentUser })
            user.fetch(
                success: ->
                    app.contentRegion.show(new UserEditView(model: user))
            )
            true

    DssController
