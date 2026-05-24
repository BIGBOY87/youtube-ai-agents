import time, logging
from youtube_client import YouTubeClient
from agents import ReportOrchestrator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_once():
    yt = YouTubeClient()
    channel = yt.channel()
    videos = yt.recent_videos(max_results=12)
    report = ReportOrchestrator().full_report(channel, videos, {})
    logging.info("BANG IT UP MUSIC AI Agents v2 running")
    logging.info("Channel: %s", channel.get("snippet", {}).get("title"))
    logging.info("Recent videos loaded: %s", len(videos))
    logging.info("Recommendations: %s", report["growth"]["recommendations"])

if __name__ == "__main__":
    while True:
        try: run_once()
        except Exception as e: logging.exception("Worker error: %s", e)
        time.sleep(21600)
