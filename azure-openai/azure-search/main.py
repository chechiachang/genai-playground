import os
from openai import AzureOpenAI

deployment = os.environ.get("CHAT_COMPLETIONS_DEPLOYMENT_NAME")
search_endpoint = os.environ.get("AZURE_SEARCH_ENDPOINT")
search_index = os.environ.get("AZURE_SEARCH_INDEX")

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
)

SYSTEM_PROMPT = """
你是一個圖片搜尋助手，請幫我找一張相關的圖片，並提供一個簡短描述（50 字內）。
""".strip()  # noqa

USER_PROMPT = """
請幫我搜尋 {query} 的相關圖片，並提供一個簡短描述（50 字內），請附上圖片網址
""".strip()  # noqa

try:
    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system","content": SYSTEM_PROMPT,},
            {"role": "user","content": USER_PROMPT.format(query="狗"),},
        ],
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "index_name": search_index,
                        "authentication": {
                            "type": "system_assigned_managed_identity"
                        }
                    }
                }
            ]
        }
    )
    print(completion.choices[0].message.content)
    #print(completion.model_dump_json(indent=2))

except Exception as e:
    print(e)
