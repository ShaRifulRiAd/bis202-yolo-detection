import subprocess
import sys
import os
import json
import boto3

def run_detection(image_path, bucket_name, image_key):
    """Run YOLOv5 detection on an image and save results to S3"""
    
    # Run YOLOv5
    result = subprocess.run(
        [sys.executable, 'detect.py',
         '--weights', 'yolov5s.pt',
         '--source', image_path,
         '--save-txt',
         '--nosave'],
        capture_output=True,
        text=True,
        cwd='/home/ubuntu/yolov5'
    )
    
    # Parse output
    detections = []
    for line in result.stdout.split('\n'):
        if '.jpg' in line or '.png' in line or '.jpeg' in line:
            detections.append(line.strip())
    
    # Save to S3
    s3_client = boto3.client('s3', region_name='ap-southeast-2')
    
    detection_result = {
        'image': image_key,
        'detections': detections,
        'raw_output': result.stdout,
        'status': 'complete'
    }
    
    result_key = f'results/{os.path.basename(image_key)}_results.json'
    
    s3_client.put_object(
        Bucket=bucket_name,
        Key=result_key,
        Body=json.dumps(detection_result, indent=2),
        ContentType='application/json'
    )
    
    print(f"Results saved to s3://{bucket_name}/{result_key}")
    return detection_result

if __name__ == "__main__":
    # Test the detection
    bucket = "bis202sharifulriad"
    image_key = "Gemini_Generated_Image_pf2z7pf2z7pf2z7p.png"
    
    # Download image from S3
    s3 = boto3.client('s3', region_name='ap-southeast-2')
    download_path = f'/tmp/{os.path.basename(image_key)}'
    s3.download_file(bucket, image_key, download_path)
    
    # Run detection
    results = run_detection(download_path, bucket, image_key)
    print(json.dumps(results, indent=2))