from tortoise import fields, models


class Videos(models.Model):
    id = fields.IntField(pk=True)
    video_id = fields.CharField(null=False, max_length=255, unique=True)
    title = fields.TextField(null=False)
    description = fields.TextField(null=True)
    thumbnail_url = fields.TextField(null=True)
    uploader = fields.TextField(null=True)
    published_at = fields.DatetimeField(null=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "videos"
