from django.db import models
from django.conf import settings
from osmosis.action_type.models import ActionType
from osmosis.program.models import Program

class Metric(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=64, db_index=True, help_text=("Descriptive name of this custom Metric"))
    program = models.ForeignKey(Program, related_name='metric_program', on_delete=models.PROTECT, help_text=("Program which defined this custom Metric"))
    first = models.ForeignKey(ActionType, related_name='metric_first', on_delete=models.PROTECT, help_text=("The first ActionType this Metric should follow"))
    second = models.ForeignKey(ActionType, related_name='metric_second', on_delete=models.PROTECT, null=True, help_text=("The second ActionType this Metric should follow"))
    showUser = models.BooleanField(default=False)

    def __unicode__(self):
        return  self.name