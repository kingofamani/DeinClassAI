"""LiteLLM 自訂回調函式

目前僅示範「上課時段限制」：
若當前時間 (台灣時區, UTC+8) 不在 08:00~17:00 之間，則拒絕請求。

未來可依學生 metadata 中的自訂時段、預算等條件擴充。
"""
from __future__ import annotations

import datetime
import pytz
from litellm.utils import LiteLLMValidationException  # type: ignore

TW_TZ = pytz.timezone("Asia/Taipei")
START_HOUR = 8  # 08:00
END_HOUR = 22   # 22:00


def pre_call_callback(*_, **__):  # noqa: D401,E501
    """在轉發至 OpenAI 之前觸發。

    Raise LiteLLMValidationException to block the request.
    """
    now = datetime.datetime.now(tz=TW_TZ)
    if START_HOUR <= now.hour < END_HOUR:
        return  # allow

    raise LiteLLMValidationException(
        f"請求被拒：僅允許於 {START_HOUR}:00 至 {END_HOUR}:00 期間使用。")
