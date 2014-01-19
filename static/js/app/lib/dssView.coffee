define ['marionette', 'utils'],
(Marionette, utils) ->
    class DssView extends Marionette.ItemView
        templateHelpers:
            renderCheckbox: (value) ->
                return (if value then "checked" else "")

            isMe: (id) ->
                return utils.isMe(id)

            humanise: (date)->
                moment(date).fromNow()

            secondsToHms: (d) ->
                utils.secondsToHms d

    DssView
