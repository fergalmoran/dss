define ['app', 'marionette', 'vent',
        'views/chat/chatView',
        'models/mix/mixItem', 'views/mix/mixListLayout', 'views/mix/mixListView', 'views/mix/mixDetailView'
        'views/mix/mixEditView', 'views/user/userProfileView',
        'models/user/userItem', 'views/user/userListView', 'views/user/userEditView'],
(App, Marionette, vent, ChatView, MixItem, MixListLayout, MixListView, MixDetailView, MixEditView, UserProfileView, UserItem, UserListView, UserEditView)->
    class DssController extends Marionette.Controller

        home: ->
            console.log "Controller: home"
            @showMixList()
            true

        _showMixList: () ->
            app = require('app')
            app.contentRegion.show(new MixListLayout())
            true

        showMixList: (type) ->
            @_showMixList()
            vent.trigger("mix:showlist", {order_by: type || 'latest'})
            true

        showMix: (slug)->
            console.log "Controller: showMix"
            app = require('app')
            mix = new MixItem({id: slug})
            mix.fetch(
                success: ->
                    app.contentRegion.show(new MixDetailView({model: mix}))
                    true
            )
            true

        uploadMix: ->
            console.log("Controller: mixUpload")
            app = require('app')
            mix = new MixItem({
                title: '',
                description: '',
                mix_image: '',
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
            @_showMixList()
            vent.trigger("mix:showlist", {order_by: 'latest', favourites__slug: slug})

        showUserLikes: (slug) ->
            console.log("Controller: showUserLikes")
            @_showMixList()
            vent.trigger("mix:showlist", {order_by: 'latest', likes__slug: slug})

        showUserMixes: (slug) ->
            console.log("Controller: showUserMixes")
            @_showMixList()
            vent.trigger("mix:showlist", {order_by: 'latest', user: slug})

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