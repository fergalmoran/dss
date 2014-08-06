@Dss.module "UserApp.Views", (Views, App, Backbone, Marionette, $    ) ->
    class Views.UserListView extends Marionette.CompositeView

        template: "userlistview"
        events:
            "keyup #search-text": "doSearch"

        ui:
            searchText: "#search-text"

        className: "row"
        childView: Views.UserItemView
        childViewContainer: "#user-table"
        initialize: (options) =>
            console.log "UserListView: initialize"
            @collection = new App.UserApp.Models.UserCollection()
            @_fetchCollection(options)
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

        onRender: ->
            window.scrollTo 0, 0

    Views.UserListView
