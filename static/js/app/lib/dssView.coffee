define ['marionette', 'utils'],
(Marionette, utils) ->
    class DssView extends Marionette.ItemView
        templateHelpers:
            renderCheckbox: (value) ->
                return (if value then "checked" else "")

            humanise: (date)->
                moment(date).fromNow()

    DssView