import unittest
from app import app

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client and propagate the exceptions to the test client
        app.testing = True
        self.app = app.test_client()

    def test_confirm_reservation_success(self):
        # Send a POST request
        response = self.app.post('/confirm_reservation', json={
            "slot": "2023-08-13 08:15",
            "client_id": "client123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "Reservation confirmed"})

    def test_confirm_reservation_failure(self):
        # Send a POST request with wrong data
        response = self.app.post('/confirm_reservation', json={
            "slot": "2023-08-13 09:00",
            "client_id": "client456"
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Reservation not found or already expired"})

    def test_confirm_reservation_missing_data(self):
        # Test missing client_id
        response = self.app.post('/confirm_reservation', json={
            "slot": "2023-08-13 08:15"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Missing slot or client_id"})

if __name__ == "__main__":
    unittest.main()