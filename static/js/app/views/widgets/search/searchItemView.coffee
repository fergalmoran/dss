define ['jquery', 'underscore', 'app.lib/dssView', 'vent',
        'text!/tpl/SearchResultViewMix',
        'typeahead'],
($, _, DssView, vent, Template) ->
    class SearchItemView extends DssView
        template: _.template(Template)
        el: "li"

        templateHelpers:
            humanise: (date)->
                moment(date).fromNow()

    SearchItemView