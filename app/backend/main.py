from fastapi import FastAPI, Form, File, UploadFile
from datetime import date
import boto3
import json
import os

app = FastAPI(title="MediVault API")

S3_BUCKET = "medivault-scan-images-bucket01"

s3 = boto3.client("s3")


@app.get("/")
def root():
    return {
        "application": "MediVault",
        "status": "running"
    }


@app.post("/patients/{patient_id}/scan")
async def upload_scan(
    patient_id: str,
    patient_name: str = Form(...),
    gender: str = Form(...),
    age: int = Form(...),
    scan_date: date = Form(...),
    image: UploadFile = File(...)
):

    # S3 key for image
    image_key = (
        f"scans/{patient_id}/image/{image.filename}"
    )

    # Read image
    image_data = await image.read()

    # Upload image to S3
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=image_key,
        Body=image_data,
        ContentType=image.content_type
    )

    # Patient metadata
    patient_info = {
        "patient_id": patient_id,
        "patient_name": patient_name,
        "gender": gender,
        "age": age,
        "scan_date": str(scan_date),
        "image": image_key
    }

    # Convert JSON to bytes
    patient_info_data = json.dumps(
        patient_info,
        indent=4
    ).encode("utf-8")

    # S3 key for metadata
    info_key = (
        f"scans/{patient_id}/patient_info/info.json"
    )

    # Upload metadata
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=info_key,
        Body=patient_info_data,
        ContentType="application/json"
    )

    return {
        "message": "Scan uploaded successfully",
        "patient_id": patient_id,
        "image": image_key,
        "patient_info": info_key
    }