from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.provider import LLMResponse, ProviderRequest
from astrbot.api.star import Context, Star, register


INJECT_PROMPT = """
<no_reply_instruction>
当你判断当前消息不需要回复时（例如消息是发给别人的、没有实际问题、群聊中不需要你发言、或者你没有合适的内容要说），只输出 <<NO_REPLY>>，不要输出任何其他内容。
当你有正常内容要回复时，正常回复即可，不要包含 <<NO_REPLY>>。
</no_reply_instruction>
""".strip()


@register("no_reply_filter", "hdhyhjfhjd", "当模型输出包含 <<NO_REPLY>> 时拦截消息不发送；并自动注入提示词引导模型在无需回复时输出标记", "1.1")
class NoReplyFilter(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.on_llm_request()
    async def inject_no_reply_hint(self, event: AstrMessageEvent, req: ProviderRequest):
        # 每次 LLM 请求前，往 system prompt 末尾追加 no_reply 提示词
        req.system_prompt = (req.system_prompt or "") + "\n" + INJECT_PROMPT

    @filter.on_llm_response()
    async def on_llm_response(self, event: AstrMessageEvent, resp: LLMResponse):
        # 当模型输出包含 <<NO_REPLY>> 时，拦截该消息，不发送给用户
        # upper() 做大小写不敏感匹配，兼容 <<no_reply>> 等写法
        if "<<NO_REPLY>>" in resp.completion_text.upper():
            event.stop_event()
