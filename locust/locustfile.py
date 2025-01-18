from locust import HttpUser, task, between, tag

class WebTestUser(HttpUser):
    wait_time = between(1, 2)
    test_data = {"message": "test data", "number": 42}
    
    @tag('aiohttp', 'with-cookie', 'all')
    @task(1)
    def test_aiohttp_with_cookie(self):
        with self.client.post(
            "http://localhost:8080/",
            json=self.test_data,
            cookies={"ctest": "1"},
            catch_response=True
        ) as response:
            if response.text == "OK":
                response.success()
            else:
                response.failure("Got wrong response")

    @tag('aiohttp', 'no-cookie', 'all')
    @task(1)
    def test_aiohttp_without_cookie(self):
        with self.client.post(
            "http://localhost:8080/",
            json=self.test_data,
            catch_response=True
        ) as response:
            if response.text == "OK":
                response.success()
            else:
                response.failure("Got wrong response")
    
    @tag('flask', 'with-cookie', 'all')
    @task(1)
    def test_flask_with_cookie(self):
        with self.client.post(
            "http://localhost:5000/",
            json=self.test_data,
            cookies={"ctest": "1"},
            catch_response=True
        ) as response:
            if response.text == "OK":
                response.success()
            else:
                response.failure("Got wrong response")

    @tag('flask', 'no-cookie', 'all')
    @task(1)
    def test_flask_without_cookie(self):
        with self.client.post(
            "http://localhost:5000/",
            json=self.test_data,
            catch_response=True
        ) as response:
            if response.text == "OK":
                response.success()
            else:
                response.failure("Got wrong response")

    @tag('express', 'with-cookie', 'all')
    @task(1)
    def test_express_with_cookie(self):
        with self.client.post(
            "http://localhost:3000/",
            json=self.test_data,
            cookies={"ctest": "1"},
            catch_response=True
        ) as response:
            if response.text == "OK":
                response.success()
            else:
                response.failure("Got wrong response")

    @tag('express', 'no-cookie', 'all')
    @task(1)
    def test_express_without_cookie(self):
        with self.client.post(
            "http://localhost:3000/",
            json=self.test_data,
            catch_response=True
        ) as response:
            if response.text == "OK":
                response.success()
            else:
                response.failure("Got wrong response")

