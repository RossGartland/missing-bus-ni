import unittest
from app import app
from unittest.mock import patch
from flask import url_for

class TestFlaskApp(unittest.TestCase):
    """Test Flask routes"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        """Test index page loads successfully"""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bus Information Form", response.data)

    @patch("services.db_service.save_report")
    def test_submit_form(self, mock_save_report):
        """Test submitting the form"""
        mock_save_report.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

        response = self.app.post("/submit", data={
            "busNumber": "123",
            "stopName": "Main St",
            "date": "2025-02-07",
            "time": "12:00",
            "email": "test@example.com",
            "additionalInfo": "Late bus"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()