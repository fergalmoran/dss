define ['backbone', 'models/user/userItem', 'app.lib/backbone.dss.model.collection'], \
    (Backbone, UserItem, DssCollection) ->
        class UserCollection extends DssCollection
            page: 0
            limit: 20
            model: UserItem
            url: ->
                com.podnoms.settings.urlRoot + "user/?limit=" + @limit + "&offset=" + @page * @limit

            _columns: [
                property: 'last_login'
                label: 'Name'
                sortable: true
            ,
                property: 'uploads'
                label: 'Uploads'
                sortable: true
            ,
                property: 'likes'
                label: 'Likes'
                sortable: true
            ,
                property: 'favourites'
                label: 'Favourites'
                sortable: true
            ,
                property: 'followers'
                label: 'Followers'
                sortable: true
            ,
                property: 'following'
                label: 'Following'
                sortable: true
            ,
                property: 'lastseen'
                label: 'Last seen'
                sortable: true
            ]

            columns: ->
                console.log("UserCollection: columns")
                @_columns

            data: ->
                console.log("UserCollection: data")
                @toJSON()

            formatter: (items) ->
                console.log("UserCollection: formatter")
                $.each items, (index, item) ->
                    item.image = '<img src="' + flickrUrl(item) + '"></a>'

        UserCollection

