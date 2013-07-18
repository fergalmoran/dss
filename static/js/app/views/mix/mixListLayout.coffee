define [
    'marionette', 'vent',
    'models/user/userItem',
    'views/widgets/mixTabHeaderView', 'views/user/userItemView', 'views/mix/mixListView',
    'text!/tpl/MixListLayoutView'],
(Marionette, vent,
 UserItem,
 MixTabHeaderView, UserItemView, MixListView,
 Template) ->

    class MixListRegionView extends Marionette.Layout
        template: _.template(Template)
        regions:{
            headerRegion: "#mix-list-heading"
            bodyRegion: "#mix-list-body"
        }

        initialize: ->
            @listenTo(vent, "mix:showlist", @showMixList)
            @listenTo(vent, "user:showdetail", @showUserView)

        onShow: ->
            @headerRegion.show(new MixTabHeaderView())

        showMixList: (options)->
            @bodyRegion.show(new MixListView(options))

        showUserView: (options) ->
            @bodyRegion.show(new MixListView(options))
            user = new UserItem({id: options.user})
            user.fetch(
                success: =>
                    @headerRegion.show(new UserItemView({model: user}))
            )
    MixListRegionView