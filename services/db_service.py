import boto3
import uuid
from config import AWS_REGION, DYNAMO_TABLE_NAME
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMO_TABLE_NAME)

def save_report(bus_number, stop_name, date, time, email, additional_info, reason):

    report_id = str(uuid.uuid4())

    response = table.put_item(
        Item={
            "ReportId": report_id,
            "BusNumber": bus_number,
            "Reason": reason,
            "StopName": stop_name,
            "Date": date,
            "Time": time,
            "Email": email,
            "AdditionalInfo": additional_info,
            'Timestamp': datetime.now().isoformat() 
        }
    )
    return response

def get_recent_reports(limit=6):

    response = table.scan()  
    reports = response.get("Items", [])

    reports.sort(key=lambda x: x.get("Timestamp", 0), reverse=True)

    return reports[:limit] 