# import eventlet
# from eventlet import wsgi

# eventlet.monkey_patch()

from app import app


if __name__ == "__main__":
    # wsgi.server(eventlet.listen(("", 5000)), app)
    app.run(debug=True)
