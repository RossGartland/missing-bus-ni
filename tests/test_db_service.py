import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from services.db_service import save_report, get_recent_reports

class TestDynamoService(unittest.TestCase):
    """Test DynamoDB service methods using mocks"""

    @patch("services.db_service.table")
    def test_get_recent_reports(self, mock_table):
        """Test retrieving recent reports with mocked DynamoDB"""
        now = int(datetime.now(timezone.utc).timestamp())

        mock_table.scan.return_value = {
            "Items": [
                {"BusNumber": "123", "Timestamp": now - 10, "Reason": "Bus was late"},
                {"BusNumber": "456", "Timestamp": now, "Reason": "Bus did not show"},
            ]
        }

        reports = get_recent_reports(limit=2)

        mock_table.scan.assert_called_once()

        self.assertEqual(len(reports), 2)
        self.assertEqual(reports[0]["BusNumber"], "456")  
        self.assertEqual(reports[1]["BusNumber"], "123")  

if __name__ == "__main__":
    unittest.main()
