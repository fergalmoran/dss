define ['jquery', 'underscore', 'libs/bootstrap/bootstrap-typeahead', 'marionette', 'vent', 'text!/tpl/SearchView',
        'text!/tpl/SearchResultView'],
($, _, Typeahead, Marionette, vent, Template, SearchResultView) ->
    class SearchView extends Marionette.CompositeView
        template: _.template(Template)

        ui:
            searchText: '#search-text'

        engine:
            compile: (template) ->
                compiled = _.template(template)
                render: (context) ->
                    compiled context

        onShow: ->
            console.log("SearchView: onShow")
            t = $('#search-text', @el).typeahead
                name: "search"
                engine: @engine
                valueKey: "title"
                template: SearchResultView
                remote:
                    url: "/api/v1/mix/search?q=%QUERY"
                    dataType: "json"
                    filter: (parsedResponse)->
                        parsedResponse.objects

            $('.tt-hint', @el).addClass('search-query');
            $('.tt-hint', @el).addClass('span3');

            t.on 'typeahead:selected': (event, datum, dataset_name) ->
                console.log("SearchView: Selected")
                vent.trigger 'navigate:mix', datum.slug
                $('#search-text', @el).blur()
                $('.tt-hint', @el).blur()
    SearchView