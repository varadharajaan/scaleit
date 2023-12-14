from flask import Flask
from flask_principal import Principal
from flasgger import Swagger
import threading
import click
from autoscaler_service import auto_scale
from config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SWAGGER'] = Config.SWAGGER_CONFIG

principal = Principal(app)
swagger = Swagger(app)


@click.command()
@click.option('--port', default=8213, help='Specify the port (default: 8213)')
def run(port):
    app.run(debug=True, port=port)


if __name__ == '__main__':
    # Start the auto-scaling logic in a separate thread
    auto_scale_thread = threading.Thread(target=auto_scale)
    auto_scale_thread.start()
    run()
