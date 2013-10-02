define ['vent', 'socket.io'],
(vent, SocketIO)  ->
    class RealtimeController
        startSocketIO: ->
            console.log("RealtimeController: SocketIO starting on " + com.podnoms.settings.REALTIME_HOST)
            @socket = SocketIO.connect(com.podnoms.settings.REALTIME_HOST)
            @socket.on "hello", (data) =>
                console.log("RealtimeController: Connected " + data['message'])

            """
            @socket.on "activity", (data) =>
                console.log("RealtimeController: activity " + data['message'])
                vent.trigger("model:activity:new", data['message'])
            """

            @socket.on "notification", (data) =>
                console.log("RealtimeController: notification " + data['message'])
                vent.trigger("model:notification:new", data['message'])

        sendMessage: (message) ->
            console.log("RealtimeController: sendMessage")
            console.log(message)

    RealtimeController

