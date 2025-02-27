from flask import Flask, request, jsonify
from ariadne import QueryType, make_executable_schema, graphql_sync

# Define the GraphQL Playground HTML manually
PLAYGROUND_HTML = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset=utf-8/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GraphQL Playground</title>
    <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css" />
    <link rel="shortcut icon" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/favicon.png" />
    <script src="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
  </head>
  <body>
    <div id="root"></div>
    <script>
      window.addEventListener('load', function (event) {
        GraphQLPlayground.init(document.getElementById('root'), {
          endpoint: '/graphql'
        })
      })
    </script>
  </body>
</html>
"""

# Define GraphQL type definitions and resolvers
type_defs = """
    type Query {
        hello(name: String): String!
    }
"""

query = QueryType()


@query.field("hello")
def resolve_hello(_, info, name=None):
    return f"Hello, {name or 'stranger'}!"


# Create the executable schema
schema = make_executable_schema(type_defs, query)

# Initialize Flask app
app = Flask(__name__)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # Return the GraphQL Playground for GET requests
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # Handle POST requests for GraphQL queries
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)
