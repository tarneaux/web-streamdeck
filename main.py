import flask
import json
import os
import threading

start = """
<!DOCTYPE html>
<html>
<head>
<title>Soundboard</title>
</head>
<body>
<p>
"""
end = """
</p>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script>
$("*").each(function() {
    if (this.id) {
        this.addEventListener("click", function() {
            $.get("/" + this.id);
        });
    }
});
</script>
</body>
</html>
"""

class Soundboard:
    def __init__(self):
        self.app = flask.Flask(__name__)
        @self.app.route("/")
        def index():
            self.refresh_widgets()
            return start + "\n".join(["<img id=\"{}\" src=\"{}\" width=128></img>".format(link, widget["icon"]) for link, widget in zip(self.links, self.widgets)]) + end
        @self.app.route("/<link>")
        def run(link):
            widget = self.widgets[int(link)]
            threading.Thread(target = lambda: os.system(widget["action"])).start()
            return ""
    def refresh_widgets(self):
        self.widgets = json.load(open("widgets.json"))
        self.links = list(range(len(self.widgets)))


if __name__ == "__main__":
    soundboard = Soundboard()
    soundboard.app.run(host="0.0.0.0", port=5000)
