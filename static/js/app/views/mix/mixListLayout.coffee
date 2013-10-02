define [
    'marionette', 'vent',
    'models/user/userItem', 'models/mix/mixCollection'
    'views/widgets/mixTabHeaderView', 'views/user/userItemView', 'views/mix/mixListView',
    'text!/tpl/MixListLayoutView'],
(Marionette, vent,
 UserItem, MixCollection,
 MixTabHeaderView, UserItemView, MixListView,
 Template) ->
    class MixListLayout extends Marionette.Layout
        template: _.template(Template)
        regions: {
            headerRegion: "#mix-list-heading"
            bodyRegion: "#mix-list-body"
        }

        initialize: ->
            @listenTo(vent, "mix:showlist", @showMixList)
            @listenTo(vent, "user:showdetail", @showUserView)
            @showMixList(@options)

        onShow: ->
            @headerRegion.show(new MixTabHeaderView())

        showMixList: (options)->
            @collection = new MixCollection()
            @collection.fetch
                data: @options
                success: (collection)=>
                    @bodyRegion.show(new MixListView({collection: collection}))

        showUserView: (options) ->
            @bodyRegion.show(new MixListView(options))
            user = new UserItem({id: options.user})
            user.fetch(
                success: =>
                    @headerRegion.show(new UserItemView({model: user}))
            )

    MixListLayout