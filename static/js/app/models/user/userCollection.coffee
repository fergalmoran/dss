define ['backbone', 'models/user/userItem', 'app.lib/backbone.dss.model.collection'], \
    (Backbone, UserItem, DssCollection) ->
        class UserCollection extends DssCollection
            model: UserItem
            url:com.podnoms.settings.urlRoot + "user/"

            _columns: [
                property: 'toponymName'
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
                @_columns

            data: ->
                @toJSON

        UserCollection

