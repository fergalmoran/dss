define ['app', 'marionette',
        'models/mix/mixItem', 'views/mix/mixListView', 'views/mix/mixDetailView', 'views/mix/mixEditView',
        'models/user/userItem', 'views/user/userEditView'],
(App, Marionette, MixItem, MixListView, MixDetailView, MixEditView, UserItem, UserEditView)->
    class DssController extends Marionette.Controller
        home: ->
            console.log "Controller: home"
            @showMixList()
            true

        showMixList: (type, options) ->
            console.log "Controller: showMixList"
            type = type or "latest"
            app = require('app')

            app.contentRegion.show(new MixListView($.extend({type: type}, options)), 'drop');
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

        user: (slug) ->
            @showMixList('latest', {user: slug})

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