from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import MiniMaxChat
from langchain_community.utilities import WikipediaAPIWrapper

# import os

def generate_script(subject, video_length, creativity, minimax_api_key, minimax_group_id):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             ```{wikipedia_search}```""")
        ]
    )

    model = MiniMaxChat(model="abab6.5s-chat", minimax_api_key=minimax_api_key, minimax_group_id=minimax_group_id, temperature=creativity)

    title_chain = title_template | model
    script_chain = script_template | model

    title = title_chain.invoke({"subject": subject}).content

    search = WikipediaAPIWrapper(lang="zh")
    search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length,
                                  "wikipedia_search": search_result}).content

    return search_result, title, script

# print(generate_script("sora模型", 1, 0.7, minimax_api_key="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiLmrablmagiLCJVc2VyTmFtZSI6IuatpuWZqCIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxODEwNTMwOTYxMjcyNjA3NDA3IiwiUGhvbmUiOiIxODg3NDk3NDYwNyIsIkdyb3VwSUQiOiIxODEwNTMwOTYxMjY4NDEzMDM4IiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjQtMDktMDMgMTU6MTA6NDAiLCJpc3MiOiJtaW5pbWF4In0.MXSILoIT6IlPdbubEkU7Oq0WzN5PdYEaop_6_-J1X0WVPo17BF4ylLk7YZQrE3xut23FGeNiti7Cuj1kLflu4w6Nzyfd2WDDKiOKlzg-9Wdl2p7fmc2lMn6zlz9bA2fQ-Udwz4D_kBfEKYGt5Hl3fqX6769FPl0jVCrgDV5nrlx6iwyz0iDz9w1oOiYoGTPGPFmxLhx38C0VlI-ACDLQk0NyHq6dOgHXooaonN2nk6_TLwM0GuZ4qRTP4FXNS6tpOLPB6kRJyH40MtUlur1bl1YWwXrXprCmkETNaqA16fPPfURBw7uZXyssgiTxkUEblpuq9fl7SzVA7FSozOpiug", minimax_group_id="1810530961268413038"))