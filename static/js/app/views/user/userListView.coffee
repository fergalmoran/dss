define ['jquery', 'marionette', 'models/user/userCollection', 'views/user/userItemView', 'text!/tpl/UserListView',
        'libs/bootstrap/bootpag'],
($, Marionette, UserCollection, UserItemView, Template) ->
    class UserListView extends Marionette.CompositeView

        template: _.template(Template)
        events:
            "keyup #search-text": "doSearch"

        ui:
            searchText: "#search-text"

        itemView: UserItemView
        itemViewContainer: "tbody"

        isLoading = true

        initialize: =>
            console.log "UserListView: initialize"
            @collection = new UserCollection()
            @_fetchCollection(@options)
            return

        _fetchCollection: (options)=>
            @collection.fetch(
                data: options
                success: =>
                    console.log("UserListView: Collection fetched")
                    console.log(@collection)
                    pag = $("#page-selection").bootpag
                        total: @collection.page_count

                    pag.on "page", (event, num) => # page number here
                        console.log "Paginating"
                        @collection.page = num # Load next page
                        @collection.fetch()
                    @isLoading = false
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