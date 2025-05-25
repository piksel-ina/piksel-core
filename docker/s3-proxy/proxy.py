from flask import Flask, Response, request, jsonify
import boto3
from botocore.exceptions import ClientError
import os

app = Flask(__name__)

BUCKET_NAME = 'usgs-landsat'  
AWS_REGION = 'us-west-2'      

# Initialize S3 client 
s3_client = boto3.client('s3', region_name=AWS_REGION)

@app.route('/health')
def health():
    return {'status': 'working'}

@app.route('/data/<path:object_key>')
def get_landsat_file(object_key):
    print(f"Requesting: {object_key}")
    
    try:
        # Get file from USGS Landsat bucket
        response = s3_client.get_object(
            Bucket=BUCKET_NAME,
            Key=object_key,
            RequestPayer='requester'  
        )
        
        # Send file back to JupyterLab
        return Response(
            response['Body'].read(),
            mimetype='application/octet-stream'
        )
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            return jsonify({'error': 'File not found'}), 404
        else:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
