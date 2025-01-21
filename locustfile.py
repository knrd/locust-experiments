from locust import HttpUser, task, between, tag
from locust.exception import RescheduleTask
from threading import Lock
import logging


class SharedState:
    """Class to store shared session ID across users"""
    session_id = None
    is_session_id_retrieved = False
    lock = Lock()


class WebTestUser(HttpUser):
    wait_time = between(1, 2)
    test_data = {"message": "test data", "number": 42}
    # shared_state = SharedState()

    # def get_session_id(self):
    #     """Perform login and store session ID"""
    #     response = self.client.post(
    #         "/login",
    #         json={
    #             "username": "your_username",
    #             "password": "your_password"
    #         }
    #     )
        
    #     # Assuming the session ID is returned in a cookie or response header
    #     # Modify this according to your API's response format
    #     self.shared_state.session_id = response.cookies.get('session_id')  # Or response.headers.get('X-Session-ID')
        
    #     if not self.shared_state.session_id:
    #         raise Exception("Failed to get session ID")

    # def on_start(self):
    #     """Called when a User starts"""
    #     # Only get the session ID if we haven't retrieved it yet
    #     logging.info("EVERY TIME ON START")
    #     if not self.shared_state.is_session_id_retrieved:
    #         with self.shared_state.lock:  # Use lock to prevent race conditions
    #             if not self.shared_state.is_session_id_retrieved:
    #                 self.get_session_id()
    #                 logging.info("ONLY ONCE")
    #                 self.shared_state.is_session_id_retrieved = True
    
    @tag('flask', 'with-cookie', 'all')
    @task(1)
    def test_flask_with_cookie(self):
        logging.info("LOG: test_flask_with_cookie(self)")
        self.client.post(
            "/flask/",
            json=self.test_data,
            cookies={"ctest": "1"},
        )

    @tag('flask', 'no-cookie', 'all')
    @task(1)
    def test_flask_without_cookie(self):
        self.client.post(
            "/flask-nc/",
            json=self.test_data,
        )

    @tag('aiohttp', 'with-cookie', 'all')
    @task(1)
    def test_aiohttp_with_cookie(self):
        self.client.post(
            "/aiohttp/",
            json=self.test_data,
            cookies={"ctest": "1"}
        )

    @tag('aiohttp', 'no-cookie', 'all')
    @task(1)
    def test_aiohttp_without_cookie(self):
        self.client.post(
            "/aiohttp-nc/",
            json=self.test_data,
        )

    @tag('express', 'with-cookie', 'all')
    @task(1)
    def test_express_with_cookie(self):
        self.client.post(
            "/express/",
            json=self.test_data,
            cookies={"ctest": "1"},
        )

    @tag('express', 'no-cookie', 'all')
    @task(1)
    def test_express_without_cookie(self):
        self.client.post(
            "/express-nc/",
            json=self.test_data,
        )
