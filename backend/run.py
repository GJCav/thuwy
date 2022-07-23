from os import environ

if not environ.get("DEBUG"):
    import eventlet
    eventlet.monkey_patch()


from app import socketio_app, app


if __name__ == "__main__":
    socketio_app.run(app)
