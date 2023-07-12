"""
Murloc is an extensible API server.

To define API methods, use the route decorator like so:

```python
# file: main.py
from murloc import Murloc

app = Murloc()

@app.route("/hello")
def hello_world():
    return "hello, world!"

@app.route("/echo")
def echo_data(data):
    return data
```

You can also specify `methods` directly as a dict() during Murloc initialization:

```python
# file: main.py
from murloc import Murloc

def hello_world():
    return "hello, world!"

def echo_data(data):
    return data

app = Murloc(methods={"/hello": hello_world, "/echo": echo_data})
```

Run murloc with uvicorn like so:

$ uvicorn main:app

Or, with gunicorn (must support ASGI) like so:

$ gunicorn main:app --worker-class uvicorn.workers.UvicornWorker

Note: Assumes main.py and the Murloc variable `app`.
"""
from .murloc import Murloc
