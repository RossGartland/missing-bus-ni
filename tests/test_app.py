import unittest
from unittest.mock import patch
from datetime import datetime, timezone
from app import app, get_reason_class
from services.db_service import save_report

class TestFlaskApp(unittest.TestCase):
    """Test Flask routes"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    @patch("app.get_recent_reports")
    def test_index_page(self, mock_get_reports):
        """Test index page loads successfully and displays reports"""
        mock_get_reports.return_value = [
            {
                "BusNumber": "143",
                "StopName": "Central Ave",
                "Reason": "Bus did not show",
                "Date": "2024-02-06",
                "Time": "08:30 AM",
                "AdditionalInfo": "Had to take a taxi",
                "created_at": datetime.now(timezone.utc)
            }
        ]

        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"143", response.data) 
        self.assertIn(b"Bus did not show", response.data) 

    @patch("app.save_report")
    def test_submit_form(self, mock_save_report):
        """Test submitting the form"""
        mock_save_report.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

        response = self.app.post("/submit", data={
            "busNumber": "123",
            "stopName": "Main St",
            "date": "2024-02-07",
            "time": "12:00 PM",
            "email": "test@example.com",
            "additionalInfo": "Late bus",
            "reason": "Bus was late"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        mock_save_report.assert_called_once_with(
            "123", "Main St", "2024-02-07", "12:00 PM", "test@example.com", "Late bus", "Bus was late"
        )

    @patch("app.save_report")
    def test_submit_form_with_other_reason(self, mock_save_report):
        """Test submitting the form with 'Other' reason"""
        mock_save_report.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

        response = self.app.post("/submit", data={
            "busNumber": "789",
            "stopName": "Elm St",
            "date": "2024-02-07",
            "time": "10:45 AM",
            "email": "user@example.com",
            "additionalInfo": "Unexpected detour",
            "reason": "Other",
            "otherReason": "Driver took an unusual route"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        mock_save_report.assert_called_once_with(
            "789", "Elm St", "2024-02-07", "10:45 AM", "user@example.com", "Unexpected detour", "Driver took an unusual route"
        )

    def test_get_reason_class(self):
        """Test that get_reason_class returns correct Bootstrap classes"""
        self.assertEqual(get_reason_class("Bus did not show"), "list-group-item-danger")
        self.assertEqual(get_reason_class("Bus was late"), "list-group-item-warning")
        self.assertEqual(get_reason_class("Bus drove past without stopping"), "list-group-item-info")
        self.assertEqual(get_reason_class("Other"), "list-group-item-secondary")
        self.assertEqual(get_reason_class("Unknown Reason"), "list-group-item-light")  # Default class

if __name__ == "__main__":
    unittest.main()
