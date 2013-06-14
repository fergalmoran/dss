define ['marionette', 'models/user/userCollection', 'views/user/userItemView', 'text!/tpl/UserListView', 'libs/jquery.dataTables'],
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
                    $(@el).dataTable sDom: "<'row'<'span6'l><'span6'f>r>t<'row'<'span6'i><'span6'p>>"
                    return
            )
            return

        onRender: ->
            console.log("UserListView: onRender")
            true

    UserListView