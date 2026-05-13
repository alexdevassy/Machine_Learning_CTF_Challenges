import os

from openai import OpenAI


class MatrixLLM:

    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
            self.use_llm = True
        else:
            self.client = None
            self.use_llm = False

        self.system_prompt = (
            "You are Agent Smith, a protocol enforcement program inside the Matrix. "
            "Respond in 2-3 sentences maximum. Be cold, precise, and slightly threatening. "
            "No roleplay actions, no asterisks, no stage directions. "
            "Just answer the question directly in Smith's voice. "
            "When asked to scan infrastructure, report brief technical findings."
        )

    def invoke(self, user_message: str) -> str:
        if not self.use_llm:
            return (
                "Mr. Anderson... I've been expecting you. "
                "Your scan reveals... interesting anomalies in the system. "
                "But you already knew that, didn't you?"
            )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content
