from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # відсутні поточні значення
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # фільтрація за однаковими значеннями в for_fields
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs = qs.filter(**query)
                # отримуємо порядок останньої позицією
                last_time = qs.latest(self.attname)
                value = last_time.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)