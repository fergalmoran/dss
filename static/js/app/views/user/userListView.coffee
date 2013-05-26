define ['marionette', 'views/user/userItemView'],
(Marionette, UserItemView) ->
    class UserListView extends Marionette.CompositeView
        template: "<h1>Hello Sailor</h1"
        itemView: UserItemView
        itemViewContainer: "#content"
        tagName: "li"


        return UserListView