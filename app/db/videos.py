from tortoise import fields, models, Tortoise


class Videos(models.Model):
    id = fields.IntField(pk=True)
    title = fields.TextField()
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "videos"
