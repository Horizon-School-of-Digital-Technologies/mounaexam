from flask import Flask, request, render_template
from prometheus_client import Counter, start_http_server

import requests

app = Flask(__name__)

REQUEST_COUNTER = Counter('my_flask_app_requests_total', 'Total number of requests received by the application')



@app.route("/")
def home():
    REQUEST_COUNTER.inc()
    return render_template("home.html")

if __name__ == '__main__':
    start_http_server(8000)  # Expose metrics on port 8000
    app.run()


@app.route("/search", methods=["POST"])
def search():

    # Get the search query
    query = request.form["q"]

    # Pass the search query to the Nominatim API to get a location
    location = requests.get(
        "https://nominatim.openstreetmap.org/search",
        {"q": query, "format": "json", "limit": "1"},
    ).json()

    # If a location is found, pass the coordinate to the Time API to get the current time
    if location:
        coordinate = [location[0]["lat"], location[0]["lon"]]

        time = requests.get(
            "https://timeapi.io/api/Time/current/coordinate",
            {"latitude": coordinate[0], "longitude": coordinate[1]},
        )

        return render_template("success.html", location=location[0], time=time.json())

    # If a location is NOT found, return the error page
    else:

        return render_template("fail.html")
if __name__ == '__main__':
    start_http_server(8000)  # Expose metrics on port 8000
    app.run()