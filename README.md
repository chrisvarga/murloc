# Murloc
Extensible api server

## Example usage
```
import murloc

# Define server methods here.
# Must have (self, params) as params.
def hello(self, params):
    self.log("hello, world!")
    return f"params={params}"


# Include method routes in this dict like so.
methods = {
    "hello": hello,
}


# Main.
# -- Include methods in murloc.init() like so.
if __name__ == "__main__":
    m = murloc.init(methods=methods)
    m.listen()
```
