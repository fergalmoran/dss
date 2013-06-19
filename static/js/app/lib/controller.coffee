define ['app', 'marionette',
        'models/mix/mixItem', 'views/mix/mixListView', 'views/mix/mixDetailView', 'views/mix/mixEditView',
        'models/user/userItem', 'views/user/userListView', 'views/user/userEditView'],
(App, Marionette, MixItem, MixListView, MixDetailView, MixEditView, UserItem, UserListView, UserEditView)->
    class DssController extends Marionette.Controller
        home: ->
            console.log "Controller: home"
            @showMixList()
            true

        _showMixList: (options) ->
            console.log "Controller: _showMixList"
            app = require('app')
            app.contentRegion.show(new MixListView(options))
            true

        showMixList: (type) ->
            @_showMixList({order_by: type || 'latest'})
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

        showUserList: (type) ->
            console.log("Controller: showUserList")
            app = require('app')
            app.contentRegion.show(new UserListView())

        showUserDetail: (slug) ->
            console.log("Controller: showUserDetail")
            @_showMixList({order_by: 'latest', user: slug})

        showUserFavourites: (slug) ->
            console.log("Controller: showUserFavourites")
            @_showMixList({order_by: 'latest', type: 'favourites', user: slug})

        showUserLikes: (slug) ->
            console.log("Controller: showUserLikes")
            @_showMixList({order_by: 'latest', type: 'likes', user: slug})

        showUserFollowing: (slug) ->
            console.log("Controller: showUserFollowing")
            @_showMixList({order_by: 'latest', type: 'following', user: slug})

        showUserFollowers: (slug) ->
            console.log("Controller: showUserFollowers")
            @_showMixList({order_by: 'latest', type: 'followers', user: slug})

        editUser: () ->
            console.log("Controller: editUser")
            app = require('app')
            user = new UserItem({id: com.podnoms.settings.currentUser })
            user.fetch(
                success: ->
                    app.contentRegion.show(new UserEditView(model: user))
            )
            true

    DssController