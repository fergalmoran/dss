define ['marionette', 'views/user/userItem'],
(Marionette, UserItemView) ->

    class UserListView extends Marionette.CompositeView
        template: "<h1>Hello Sailor</h1"
        itemView: UserItemView
        itemViewContainer: "#content"
        tagName: "li"

        initialize: ->
            console.log "User list view initializing"

        return UserListView