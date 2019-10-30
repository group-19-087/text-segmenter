# text-segmenter
Text segmenting Flask API 
This is the  API called from the v-tutor backend after a video has been successfully transcribed. ALong with the API request the transcription ID is passed. The transcription is then segmented based on the trained topic model. For a successful response output will be in following format:
```
{
  "status": number,
  "result": {
    "timestamps": [number] (segmentation points in milliseconds),
    "transcript": string,
    "keywords": [string]
  }
}
```

