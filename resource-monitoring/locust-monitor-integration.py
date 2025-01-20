from locust import HttpUser, task, events
import requests
from locust.argument_parser import setup_parser_arguments

class MyUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Access environment variables and custom arguments
        self.test_tag = self.environment.parsed_options.tag
        self.custom_arg = self.environment.parsed_options.custom_arg

    def on_start(self):
        # Start monitoring with test metadata
        monitoring_data = {
            'tag': self.test_tag,
            'custom_arg': self.custom_arg,
            'host': self.host,
            'user_count': self.environment.runner.target_user_count
        }
        requests.post('http://your-server:5000/monitor/start', json=monitoring_data)

    def on_stop(self):
        # Stop monitoring with test metadata
        monitoring_data = {
            'tag': self.test_tag,
            'custom_arg': self.custom_arg
        }
        requests.post('http://your-server:5000/monitor/stop', json=monitoring_data)

    @task
    def my_task(self):
        self.client.get("/")

# Add custom command line arguments
def setup_custom_arguments(parser):
    parser.add_argument(
        '--custom-arg',
        dest='custom_arg',
        default='default_value',
        help='Custom argument for test identification'
    )

# Register the custom arguments
@events.init_command_line_parser.add_listener
def init_parser(parser):
    setup_custom_arguments(parser)
