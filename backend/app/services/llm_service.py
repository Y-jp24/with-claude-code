from typing import Literal
import openai
import google.generativeai as genai
import anthropic
from ..core.config import settings

# LLMクライアントの初期化
openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
anthropic_client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY) if settings.CLAUDE_API_KEY else None
if settings.GOOGLE_API_KEY:
    genai.configure(api_key=settings.GOOGLE_API_KEY)

async def generate_requirement(
    idea_content: str,
    idea_title: str,
    llm_model: Literal["openai", "google", "claude"]
) -> str:
    """
    アイデアから要件定義書を生成する
    """
    prompt = f"""
以下のアイデアから、詳細な要件定義書を作成してください。

タイトル: {idea_title}
内容: {idea_content}

要件定義書には以下の項目を含めてください：
1. 概要
2. 目的と背景
3. 機能要件
   - 必須機能
   - オプション機能
4. 非機能要件
   - パフォーマンス
   - セキュリティ
   - 可用性
5. システム構成
6. 開発スケジュール（概算）
7. リスクと対策

日本語で、専門的かつ分かりやすく記述してください。
"""

    if llm_model == "openai":
        if not openai_client:
            raise ValueError("OpenAI API key is not configured")
        
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは優秀なシステムアナリストです。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    elif llm_model == "google":
        if not settings.GOOGLE_API_KEY:
            raise ValueError("Google API key is not configured")
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    
    elif llm_model == "claude":
        if not anthropic_client:
            raise ValueError("Claude API key is not configured")
        
        response = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            temperature=0.7,
            system="あなたは優秀なシステムアナリストです。",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    else:
        raise ValueError(f"Unsupported LLM model: {llm_model}")