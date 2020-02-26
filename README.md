# learning-ai

# call the speech API
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json \
"https://speech.googleapis.com/v1/speech:recognize?key=${API_KEY}"


export GOOGLE_APPLICATION_CREDENTIALS="/Users/ronald.garciarobles/Downloads/AI-POC-OCT-2018-9edd1ce1bb4c.json"
export API_KEY=