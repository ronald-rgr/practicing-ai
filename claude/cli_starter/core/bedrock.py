import boto3
from typing import Optional, Union, Dict
from mcp.types import Tool, PromptMessage, TextContent


class Bedrock:
    def __init__(self, region_name: str, model_id: str):
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        self.model_id = model_id
        self.region_name = region_name

    def add_user_message(self, messages: list, content: Union[str, list]):
        if isinstance(content, str):
            user_message = {"role": "user", "content": [{"text": content}]}
        else:
            user_message = {"role": "user", "content": content}
        messages.append(user_message)

    def add_assistant_message(self, messages: list, content: Union[str, list]):
        if isinstance(content, str):
            assistant_message = {
                "role": "assistant",
                "content": [{"text": content}],
            }
        else:
            assistant_message = {"role": "assistant", "content": content}
        messages.append(assistant_message)

    def chat(
        self,
        messages: list,
        system: Optional[str] = None,
        temperature: float = 1.0,
        stop_sequences: list = [],
        tools: Optional[list[Tool]] = None,
        tool_choice: str = "auto",
        text_editor: Optional[str] = None,
        thinking: bool = False,
    ) -> dict:
        params = {
            "modelId": self.model_id,
            "messages": messages,
            "inferenceConfig": {
                "temperature": temperature,
                "stopSequences": stop_sequences,
            },
        }

        if system:
            params["system"] = [{"text": system}]

        bedrock_tools = None
        if tools:
            bedrock_tools = to_bedrock_tools(tools)

        if bedrock_tools or text_editor:
            tool_choices = {
                "auto": {"auto": {}},
                "any": {"any": {}},
            }
            choice = tool_choices.get(
                tool_choice, {"tool": {"name": tool_choice}}
            )
            params["toolConfig"] = {
                "tools": bedrock_tools or [],
                "toolChoice": choice,
            }

        additional_model_fields = {}
        if text_editor:
            if "tools" not in additional_model_fields:
                additional_model_fields["tools"] = []

            additional_model_fields["tools"].append(
                {
                    "type": text_editor,
                    "name": "str_replace_editor",
                }
            )

        if thinking:
            additional_model_fields["thinking"] = {
                "type": "enabled",
                "budget_tokens": 200,
            }

        if additional_model_fields:
            params["additionalModelRequestFields"] = additional_model_fields

        response = self.client.converse(**params)

        output_content = (
            response.get("output", {}).get("message", {}).get("content", [])
        )
        if not isinstance(output_content, list):
            output_content = []

        text_parts = [
            p.get("text", "")
            for p in output_content
            if isinstance(p, dict) and "text" in p
        ]

        return {
            "parts": output_content,
            "stop_reason": response.get("stopReason", "unknown"),
            "text": "\n".join(text_parts),
        }


def to_bedrock_tools(tool_list: list[Tool]):
    return [
        {
            "toolSpec": {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": tool.inputSchema["properties"],
                        "required": tool.inputSchema["required"],
                    }
                },
            }
        }
        for tool in tool_list
    ]


def to_bedrock_messages(messages: list[PromptMessage]) -> list[Dict]:
    return [
        {"role": m.role, "content": [{"text": m.content.text}]}
        for m in messages
        if isinstance(m.content, TextContent)
    ]
