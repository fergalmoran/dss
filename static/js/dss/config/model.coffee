Backbone.AssociatedModel.extend
    base_url: ->
        temp_url = Backbone.Model::url.call(this)
        (if temp_url.charAt(temp_url.length - 1) is "/" then temp_url else temp_url + "/")

    url: ->
        @base_url()

    addError: (field, message) ->
        @errors[field] = []  if _.isUndefined(@errors[field])
        @errors[field].push message
        field

    secondsToHms: (field) ->
        d = @get(field)
        if d
            d = Number(d)
            h = Math.floor(d / 3600)
            m = Math.floor(d % 3600 / 60)
            s = Math.floor(d % 3600 % 60)
            ((if h > 0 then h + ":" else "")) + ((if m > 0 then ((if h > 0 and m < 10 then "0" else "")) + m + ":" else "0:")) + ((if s < 10 then "0" else "")) + s
        else
            "00:00:00"

