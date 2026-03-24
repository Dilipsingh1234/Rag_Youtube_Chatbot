from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


def get_youtube_transcript(video_id: str, languages=None) -> str:
    if languages is None:
        languages = ["en"]

    try:
        api = YouTubeTranscriptApi()
        transcript_data = api.fetch(video_id, languages=languages)
        transcript_text = " ".join(chunk.text for chunk in transcript_data)
        return transcript_text

    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise Exception("No transcript found for the requested language(s).")
    except VideoUnavailable:
        raise Exception("The video is unavailable.")
    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {e}")