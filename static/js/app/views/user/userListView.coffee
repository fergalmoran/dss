define ['marionette', 'models/user/userCollection', 'views/user/userItemView', 'text!/tpl/UserListView'],
(Marionette, UserCollection, UserItemView, Template) ->
    class UserListView extends Marionette.CompositeView

        template: _.template(Template)
        tagName: "table"
        className: "table table-hover"
        itemView: UserItemView

        initialize: ->
            console.log "UserListView: initialize"
            @collection = new UserCollection()
            @collection.fetch(
                data: @options
                success: =>
                    console.log("UserListView: Collection fetched")
                    $(@el).tablesorter()
                    return
            )
            return

        onRender: ->
            console.log("UserListView: onRender")
            true

    UserListView