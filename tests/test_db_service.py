import unittest
from moto import mock_aws
import boto3
from services.db_service import save_report, get_recent_reports
from config import AWS_REGION, DYNAMO_TABLE_NAME

@mock_aws
class TestDynamoService(unittest.TestCase):
    """Test DynamoDB service methods"""

    def setUp(self):
        """Set up a mocked DynamoDB table before each test"""
        self.dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
        self.table = self.dynamodb.create_table(
            TableName=DYNAMO_TABLE_NAME,
            KeySchema=[{"AttributeName": "BusNumber", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "BusNumber", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        self.table.wait_until_exists()

    def tearDown(self):
        """Clean up after each test"""
        self.table.delete()

    def test_save_report(self):
        """Test saving a report"""
        response = save_report("123", "Main St", "2025-02-07", "12:00", "test@example.com", "Late bus")
        self.assertEqual(response["ResponseMetadata"]["HTTPStatusCode"], 200)

    def test_get_recent_reports(self):
        """Test retrieving recent reports"""
        save_report("123", "Main St", "2025-02-07", "12:00", "test@example.com", "Late bus")
        reports = get_recent_reports(limit=1)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]["BusNumber"], "123")

if __name__ == "__main__":
    unittest.main()
