from django_extensions.management.jobs import HourlyJob


class Job(HourlyJob):
    help = "My sample job."

    def execute(self):
        # executing empty sample job
        print('I run every hour!!!')
        pass
