from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from app.cron.schemas import StartCronRequest
from app.utils.settings import settings
from app.utils.youtube_helper import YoutubeHelper

cron_router = APIRouter()
scheduler = BackgroundScheduler()
youtube_helper = YoutubeHelper()


@cron_router.post('/start-cron')
async def start_cron(payload: StartCronRequest):
    jobs = scheduler.get_jobs()

    cron_interval = payload.cron_interval
    search_key = payload.search_key

    for job in jobs:
        if job.next_run_time is not None:
            raise HTTPException(status_code=400,
                                detail='A job is already running. Please stop it before starting a new one')

    scheduler.add_job(youtube_helper.fetch_data, trigger=CronTrigger.from_crontab(cron_interval),
                      args=[search_key, cron_interval], id=settings.SCHEDULER_JOB_ID)
    scheduler.start()
    return {"detail": f"Cron scheduler started successfully with cron interval '{cron_interval}' "
                      f"and search key '{search_key}'"}


def stop_cron():
    scheduler.shutdown()
    print("Cron scheduler stopped successfully")


@cron_router.post('/modify-cron')
async def modify_cron(payload: StartCronRequest):
    cron_interval = payload.cron_interval
    search_key = payload.search_key

    try:
        job_id = settings.SCHEDULER_JOB_ID
        job = scheduler.get_job(job_id)

        if job:
            scheduler.pause()
            job.modify(trigger=CronTrigger.from_crontab(cron_interval), args=[search_key, cron_interval])
            scheduler.resume()
            return {"detail": f"Cron scheduler modified successfully with cron interval '{cron_interval}' "
                              f"and search key '{search_key}'"}
        else:
            raise HTTPException(status_code=404, detail="Cron job not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to modify cron scheduler: {str(e)}")


@cron_router.post('/stop-cron')
def stop_cron_endpoint():
    stop_cron()
    return {"message": "Cron scheduler stopped successfully"}
