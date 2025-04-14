# Helper functions

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from pytube import extract
import yt_dlp
from langdetect import detect


def get_video_id(url):
    return extract.video_id(url)

def get_transcript(video_id):
    """
    Get transcript for a YouTube video, prioritizing English and German languages.
    Returns the transcript text or None if no transcript is available.
    """
    try:
        # Try English first
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            return " ".join([t.get('text', '') if isinstance(t, dict) else getattr(t, 'text', '') for t in transcript])
        except NoTranscriptFound:
            # Try German if English is not available
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['de'])
                return " ".join([t.get('text', '') if isinstance(t, dict) else getattr(t, 'text', '') for t in transcript])
            except NoTranscriptFound:
                # Get list of available transcripts
                available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
                
                # Process available transcripts
                for transcript in available_transcripts:
                    try:
                        fetched = transcript.fetch()
                        # Check how to access the text based on the object type
                        if fetched and len(fetched) > 0:
                            first_item = fetched[0]
                            if isinstance(first_item, dict) and 'text' in first_item:
                                return " ".join([item['text'] for item in fetched])
                            else:
                                # Try accessing as an object attribute
                                return " ".join([getattr(item, 'text', '') for item in fetched])
                    except Exception as e:
                        print(f"Error processing transcript: {e}")
                        continue
                
                return None
            
    except Exception as e:
        print(f"[Transcript Error]: {e}")
        return None

def get_video_title(url):  
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', None)
            
            if not title:
                raise ValueError("No title found")
                
            safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-", "(", ")")).rstrip()
            return safe_title
            
    except Exception as e:
        raise ValueError(f"Could not retrieve video title with yt-dlp: {str(e)}")


def format_transcript(text, words_per_line=15):
    words = text.split()
    lines = [' '.join(words[i:i+words_per_line]) for i in range(0, len(words), words_per_line)]
    return '\n'.join(lines)


def detect_language(transcript):
    try:
        lang_code = detect(transcript)
        flags = {
            'en': '🇬🇧',
            'de': '🇩🇪',
            'fr': '🇫🇷',
            'es': '🇪🇸',
            
        }
        flag = flags.get(lang_code, '🌐')
        return lang_code, flag
    except:
        return None, '🌐'
