from flask import Flask, render_template, request
import aiml
import glob

app = Flask(__name__)


k = aiml.Kernel()

aiml_files = glob.glob('data/*.aiml')

for aiml_file in aiml_files:
    k.learn(aiml_file)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    query = request.args.get('msg')
    response = k.respond(query)
    if response:
        return (str(response))
    else:
        return (str(":)"))


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port='5000')


