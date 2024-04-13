# Videos API

## An SDK for the Videos Manipulation.

This SDK is designed to be used to manipulate videos by using latest AI models.

## Roadmap

In no strict order. Functionality added as and when requested.

### Audio Functionality
- [.] Audio Extraction 
- [.] Audio Transcription
- [ ] Speaker Diarization
- [ ] Audio Summarization
- [ ] Content Moderation
- [ ] Sentiment Analysis 
- [ ] Entiy Detection
- [ ] Auto Chapters
- [ ] PII redaction
- [ ] Remove filler words
- [ ] Remove background noise
- [ ] Dub Audio to other languages
- [ ] Text-to-Audio
- [ ] Add audio stream from text

### Text Functionality
- [ ] Generate Subtitles 
- [ ] Translate subtitles
- [ ] Add subtitle overlay
- [ ] Text Embeddings

### Video Functionailities
- [ ] Video Encoding & Decoding
- [ ] Video Embeddings
- [ ] Image-to-video https://enriccorona.github.io/vlogger/
- [ ] Fix Eye contact
- [ ] Fix lip Sync
- [ ] Remove Background
- [ ] Script to Movie

## Expected Use case

# SDK
```pytthon
    p = create_project()
    v1 = p.add_video("abc")
    v2 = p.add_video("bcd")
    p.list_videos()
    # Video Frames
    v1 = p.get_video("abc")
    v1.audio.denoise()
    v1.audio.enhance()
    v1.audio.transcribe()
    en_subs = v1.create_subtitle(lang="en")
    fr_audio = v1.audio.translate(lang="fr")
    v1.add_subtitle(en_subs, style="subtitle")
    v1_fr = v1.copy()
    v1_fr.replace_audio(fr_audio)
    v1.save("abc_modified.mp4")
    v1_fr.save("abd_fr.mp4")
```
# API

TODO