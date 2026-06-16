from flask import Flask

app = Flask(__name__)

@app.route('/')
def the_start():
    return 'beginning to the car showroom management system'

if __name__ == "__main__":
    app.run()