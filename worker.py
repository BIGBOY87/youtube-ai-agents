import time, logging, requests, os
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BASE=os.getenv('PUBLIC_BASE_URL','')
def main():
    logging.info('Starting autonomous worker. It creates drafts only; no public posting without approval.')
    while True:
        try:
            if BASE:
                r=requests.get(BASE.rstrip('/')+'/api/auto-run',timeout=60)
                logging.info('auto-run status=%s body=%s', r.status_code, r.text[:200])
            else:
                logging.info('PUBLIC_BASE_URL not set; worker idle. Set it to your Render URL to enable scheduled draft creation.')
        except Exception as e: logging.exception(e)
        time.sleep(6*60*60)
if __name__=='__main__': main()
