define ['socket.io'],
(SocketIO)  ->
    class RealtimeController
        startSocketIO: ->
            console.log("RealtimeController: Socket IO starting")
            @socket = SocketIO.connect(com.podnoms.settings.REALTIME_HOST)
            @socket.on "connect": =>
                console.log("RealtimeController: Connected")

        sendMessage: (message) ->
            console.log("RealtimeController: sendMessage")
            @socket.

    RealtimeController

