// Imports the Google Cloud client library
const speech = require('@google-cloud/speech');
const fs = require('fs');

// Creates a client
const client = new speech.SpeechClient({
    projectId: 'ai-poc-oct-2018',
    keyFilename: '/Users/ronald.garciarobles/Downloads/AI-POC-OCT-2018-9edd1ce1bb4c.json',
  });

// The name of the audio file to transcribe
const fileName = './resources/Google_Gnome.wav';

// Reads a local audio file and converts it to base64
const file = fs.readFileSync(fileName);
const audioBytes = file.toString('base64');

// The audio file's encoding, sample rate in hertz, and BCP-47 language code
const audio = {
  content: audioBytes,
};
const config = {
    encoding: 'LINEAR16',
    sampleRateHertz: 16000,
    //languageCode: 'es-CO',
    languageCode: 'en-US',
  };
const request = {
  audio: audio,
  config: config,
};

// Detects speech in the audio file
client
  .recognize(request)
  .then(data => {
    const response = data[0];
    const transcription = response.results
      .map(result => result.alternatives[0].transcript)
      .join('\n');
    console.log(`Transcription: ${transcription}`);
  })
  .catch(err => {
    console.error('ERROR:', err);
  });