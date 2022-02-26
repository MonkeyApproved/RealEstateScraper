from django_extensions.management.jobs import HourlyJob
from data_manager.models import LoadConfiguration, DataLoad
from scraping.xe import Xe
from django.utils import timezone
from logging import getLogger

logger = getLogger('Scape Job')

class Job(HourlyJob):
    help = """This job checks if there are outstanding scraping jobs.
    If there are jobs to be done they are exacuted right away.
    """

    @staticmethod
    def hours_passed(time):
        seconds_in_hour = 60 * 60
        time_passed = (timezone.now() - time)
        return round(time_passed.seconds / seconds_in_hour, 1)

    def check_collection_configs(self):
        config_list = LoadConfiguration.objects.all()
        to_be_collected = []
        for config in config_list:
            logger.info(f'>>> checking config "{config.config_name}"')
            loads = DataLoad.objects.filter(load_config=config)
            last_load = loads.order_by('-created_on').first()
            logger.info(f'  >> total of {len(loads)} data loads')
            if last_load is None:
                # this is a new config that was never collected
                logger.info(f'  >> was never run')
                to_be_collected.append(config)
                logger.info(f'  >> collection will be run')
                continue
            time_passed = self.hours_passed(last_load.created_on)
            logger.info(f'  >> time since last collection: {time_passed}h')
            if time_passed > config.frequency:
                to_be_collected.append(config)
                logger.info(f'  >> collection will be run')
            else:
                logger.info(f'  >> skipping, frequency is {config.frequency}h')
        return to_be_collected

    def run_collection(self, load_config):
        xe = Xe(
            type=load_config.item_type,
            geo_place_id=load_config.geo_place_id,
            max_price=load_config.maximum_price,
            min_year=load_config.minimum_construction_year,
            min_size=load_config.minimum_size,
        )
        xe.check_for_properties(
            load_config=load_config,
            save_to_db=True,
            save_details_to_disc=False,
        )

    def execute(self):
        logger.info('### Hourly job started: scraping properties ###')
        to_be_collected = self.check_collection_configs()
        for config in to_be_collected:
            logger.info(f'>>> running collection for "{config.config_name}"')
            self.run_collection(load_config=config)
