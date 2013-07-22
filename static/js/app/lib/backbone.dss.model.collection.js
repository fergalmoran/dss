define(['backbone'], function (Backbone) {
    return Backbone.Collection.extend({
        parse: function (response) {
            this.meta = response.meta || {};
            this.page_count = Math.ceil(this.meta.total_count / this.meta.limit);
            return response.objects || response;
        },
        /*
        sync: function (method, model, options) {
            var headers = {};

            if (Backbone.Tastypie.apiKey && Backbone.Tastypie.apiKey.username) {
                headers[ 'Authorization' ] = 'ApiKey ' + Backbone.Tastypie.apiKey.username + ':' + Backbone.Tastypie.apiKey.key;
            }

            if (Backbone.Tastypie.csrfToken) {
                headers[ 'X-CSRFToken' ] = Backbone.Tastypie.csrfToken;
            }

            // Keep `headers` for a potential second request
            headers = _.extend(headers, options.headers);
            options.headers = headers;

            if (( method === 'create' && Backbone.Tastypie.doGetOnEmptyPostResponse ) ||
                ( method === 'update' && Backbone.Tastypie.doGetOnEmptyPutResponse )) {
                var dfd = new $.Deferred();

                // Set up 'success' handling
                var success = options.success;
                dfd.done(function (resp, textStatus, xhr) {
                    _.isFunction(success) && success(resp);
                });

                options.success = function (resp, textStatus, xhr) {
                    // If create is successful but doesn't return a response, fire an extra GET.
                    // Otherwise, resolve the deferred (which triggers the original 'success' callbacks).
                    if (!resp && ( xhr.status === 201 || xhr.status === 202 || xhr.status === 204 )) { // 201 CREATED, 202 ACCEPTED or 204 NO CONTENT; response null or empty.
                        var location = xhr.getResponseHeader('Location') || model.id;
                        return Backbone.ajax({
                            url: location,
                            headers: headers,
                            success: dfd.resolve,
                            error: dfd.reject
                        });
                    }
                    else {
                        return dfd.resolveWith(options.context || options, [ resp, textStatus, xhr ]);
                    }
                };

                // Set up 'error' handling
                var error = options.error;
                dfd.fail(function (xhr, textStatus, errorThrown) {
                    _.isFunction(error) && error(xhr.responseText);
                });

                options.error = function (xhr, textStatus, errorText) {
                    dfd.rejectWith(options.context || options, [ xhr, textStatus, xhr.responseText ]);
                };

                // Create the request, and make it accessibly by assigning it to the 'request' property on the deferred
                dfd.request = Backbone.oldSync(method, model, options);
                return dfd;
            }

            return Backbone.oldSync(method, model, options);
        }
        */
    })
});
