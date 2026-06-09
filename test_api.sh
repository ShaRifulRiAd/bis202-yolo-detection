#!/bin/bash
# Test script for BIS202 Assignment 2
# Tests the API Gateway endpoint with cold start measurement

API_URL="https://xjxmwfu5w2.execute-api.ap-southeast-2.amazonaws.com/prod/detect"
BUCKET="bis202sharifulriad"
IMAGE="Gemini_Generated_Image_pf2z7pf2z7pf2z7p.png"

echo "Testing API Gateway Endpoint..."
echo "================================"

for i in 1 2 3 4 5; do
  echo "Request $i:"
  time curl -s -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d "{\"bucket\": \"$BUCKET\", \"image_key\": \"$IMAGE\"}"
  echo ""
done