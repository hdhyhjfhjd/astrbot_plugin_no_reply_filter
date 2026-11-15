from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.provider import LLMResponse
from astrbot.api.star import Context, Star, register


@register("no_reply_filter", "hdhyhjfhjd", "当模型输出包含 <<NO_REPLY>> 时，拦截消息，不发送给用户", "1.0")
class NoReplyFilter(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.on_llm_response()
    async def on_llm_response(self, event: AstrMessageEvent, resp: LLMResponse):
        # 当模型输出包含 <<NO_REPLY>> 时，拦截该消息，不发送给用户
        # upper() 做大小写不敏感匹配，兼容 <<no_reply>> 等写法
        if "<<NO_REPLY>>" in resp.completion_text.upper():
            event.stop_event()
