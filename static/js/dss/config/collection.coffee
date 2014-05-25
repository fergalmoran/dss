Backbone.Collection.prototype.parse = (response) ->
    @meta = response.meta or {}
    @page_count = Math.ceil(@meta.total_count / @meta.limit)
    response.objects or response
