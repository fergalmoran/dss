define [
    'marionette', 'vent',
    'models/user/userItem', 'models/mix/mixCollection'
    'views/widgets/mixTabHeaderView', 'views/user/userItemView', 'views/mix/mixListView', 'views/genericView',
    'text!/tpl/MixListLayoutView'],
(Marionette, vent,
 UserItem, MixCollection,
 MixTabHeaderView, UserItemView, MixListView, GenericView,
 Template) ->
    class MixListLayout extends Marionette.Layout
        template: _.template(Template)
        regions: {
            headerRegion: "#mix-list-heading"
            bodyRegion: "#mix-list-body"
        }

        initialize: (options, emptyTemplate)->
            @listenTo(vent, "mix:showlist", @showMixList)
            @listenTo(vent, "user:showdetail", @showUserView)
            @showMixList(options, emptyTemplate)

        onShow: ->
            @headerRegion.show(new MixTabHeaderView())

        showMixList: (options, emptyTemplate) ->
            @collection = new MixCollection()
            @collection.fetch
                data: options
                success: (collection)=>
                    if collection.length > 0
                        @bodyRegion.show(new MixListView({collection: collection}))
                    else
                        $.get emptyTemplate, (data) =>
                            @bodyRegion.show(new GenericView({template: data}))
        showUserView: (options) ->
            @bodyRegion.show(new MixListView(options))
            user = new UserItem({id: options.user})
            user.fetch(
                success: =>
                    @headerRegion.show(new UserItemView({model: user}))
            )

    MixListLayout