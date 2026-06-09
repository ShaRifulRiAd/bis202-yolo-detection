import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const s3Client = new S3Client({ region: "ap-southeast-2" });

export const handler = async (event) => {
    try {
        console.log('Event received:', JSON.stringify(event));
        
        // Handle both direct and API Gateway proxy events
        let bucket, imageKey;
        
        if (event.body) {
            // Coming from API Gateway
            const body = JSON.parse(event.body);
            bucket = body.bucket;
            imageKey = body.image_key;
        } else {
            // Direct invocation
            bucket = event.bucket;
            imageKey = event.image_key;
        }
        
        console.log(`Bucket: ${bucket}, Image: ${imageKey}`);
        
        // Save job record to S3
        const jobRecord = {
            bucket: bucket,
            image: imageKey,
            status: 'processing',
            timestamp: new Date().toISOString()
        };
        
        await s3Client.send(new PutObjectCommand({
            Bucket: bucket,
            Key: `jobs/${imageKey}_job.json`,
            Body: JSON.stringify(jobRecord, null, 2),
            ContentType: 'application/json'
        }));
        
        console.log('Job record saved to S3');
        
        return {
            statusCode: 200,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: 'Detection job queued successfully',
                bucket: bucket,
                image: imageKey,
                status: 'processing',
                timestamp: jobRecord.timestamp
            })
        };
        
    } catch (error) {
        console.error('Error:', error);
        return {
            statusCode: 500,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                error: error.message
            })
        };
    }
};