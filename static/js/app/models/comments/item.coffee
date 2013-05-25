define ['backbone'],
(Backbone) ->
    class CommentItem extends Backbone.Model
    urlRoot:com.podnoms.settings.urlRoot + "comments/"

    CommentItem