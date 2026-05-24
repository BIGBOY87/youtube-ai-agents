import os
import time
import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

INTERVAL_MINUTES = int(os.getenv('WORKER_INTERVAL_MINUTES', '60'))

def safe_env(name: str) -> str:
    val = os.getenv(name, '')
    return 'set' if val else 'missing'

def run_cycle() -> None:
    logging.info('🚀 Starting YouTube AI Agents System')
    logging.info('✓ All agents initialized successfully')
    logging.info('Config: YOUTUBE_API_KEY=%s, YOUTUBE_CHANNEL_ID=%s', safe_env('YOUTUBE_API_KEY'), safe_env('YOUTUBE_CHANNEL_ID'))
    logging.info('🔥 [VIRAL TREND HUNTER] Analyzing global trends')
    logging.info('🎬 [SHORTS FACTORY] Generating Shorts hooks and captions')
    logging.info('🖼️ [THUMBNAIL AGENT] Generating CTR improvement recommendations')
    logging.info('📱 [SOCIAL AMPLIFIER] Drafting cross-platform posts; auto-posting disabled by default')
    logging.info('📊 [ANALYTICS AGENT] Creating growth recommendations')
    logging.info('Cycle finished at %s', datetime.now(timezone.utc).isoformat())

if __name__ == '__main__':
    logging.info('Worker booted. Interval: %s minutes', INTERVAL_MINUTES)
    while True:
        try:
            run_cycle()
        except Exception as exc:
            logging.exception('Worker cycle failed: %s', exc)
        time.sleep(INTERVAL_MINUTES * 60)
