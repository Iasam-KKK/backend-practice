from django.utils import timezone
from .utils import fetch_token_data
from django_cron import CronJobBase, Schedule

class UpdateTokenData(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'token_fetcher.cron.UpdateTokenData'

    def do(self):
        print(f"Cron job running at {timezone.now()}")
        tokens_data = fetch_token_data()
        if tokens_data:
            print(f"Cron job updated {len(tokens_data)} tokens")
        else:
            print("Cron job failed to fetch token data")

        # Update user last_online
        from .models import UserProfile
        updated = UserProfile.objects.update(last_online=timezone.now())
        print(f"Updated {updated} user(s) last_online")