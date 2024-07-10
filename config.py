from datetime import datetime
import pytz
from pydantic import BaseModel

Tashkent_tz = pytz.timezone("Asia/Tashkent")

class BaseModel(BaseModel):
    create_at: datetime = datetime.now(tz=Tashkent_tz)
    updated_at: datetime = datetime.now(tz=Tashkent_tz)