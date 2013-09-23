define ['jquery', 'marionette', 'models/user/userCollection', 'views/user/userItemView', 'text!/tpl/UserListView',
        'bootpag'],
($, Marionette, UserCollection, UserItemView, Template) ->
    class UserListView extends Marionette.CompositeView

        template: _.template(Template)
        events:
            "keyup #search-text": "doSearch"

        ui:
            searchText: "#search-text"


        className: "row"
        itemView: UserItemView
        itemViewContainer: "#user-table"
        initialize: =>
            console.log "UserListView: initialize"
            @collection = new UserCollection()
            @_fetchCollection(@options)
            return

        _fetchCollection: (options) =>
            @collection.fetch(
                data: options
                success: =>
                    console.log("UserListView: Collection fetched")
                    return
            )

        doSearch: =>
            console.log("UserListView: doSearch")
            query = @ui.searchText.val()
            if (query)
                @_fetchCollection
                    q: query
            else
                @_fetchCollection @options

    UserListView