define ['marionette', 'models/user/userCollection', 'views/user/userItemView', 'text!/tpl/UserListView', 'libs/bootstrap/bootpag'],
(Marionette, UserCollection, UserItemView, Template) ->
    class UserListView extends Marionette.CompositeView

        template: _.template(Template)
        itemView: UserItemView
        itemViewContainer: "tbody"
        initialize: =>
            console.log "UserListView: initialize"
            @collection = new UserCollection()
            @collection.fetch(
                data: @options
                success: =>
                    console.log("UserListView: Collection fetched")
                    console.log(@collection)
                    $("#page-selection").bootpag(total: @collection.page_count).on "page", (event, num) -> # page number here
                        $("#content").html "Insert content" # some ajax content loading...
                    return
            )
            return

    UserListView