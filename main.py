from enum import Enum
from typing import Any, Optional, Union
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL_SUPPORT = "technical_support"
    ACCOUNT_ACCESS = "account_access"
    FEATURE_REQUEST = "feature_request"
    GENERAL_INQUIRY = "general_inquiry"


class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CustomerSentiment(str, Enum):
    SATISFIED = "satisfied"
    NEUTRAL = "neutral"
    FRUSTRATED = "frustrated"
    ANGRY = "angry"


class TicketAnalysis(BaseModel):
    """Structured extraction model for customer support tickets."""
    category: TicketCategory = Field(
        description="The primary domain of the issue."
    )
    urgency: UrgencyLevel = Field(
        description="Priority level based on user impact and financial/operational risk."
    )
    sentiment: CustomerSentiment = Field(
        description="Detected emotional tone of the customer."
    )
    summary: str = Field(
        description="A concise one-sentence summary of the user's core problem."
    )
    affected_product_or_feature: Optional[str] = Field(
        default=None,
        description="The specific product, feature, or page mentioned, if applicable."
    )
    suggested_action: str = Field(
        description="Immediate operational next step for the support team."
    )
    confidence_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score from 0.0 to 1.0 in this classification."
    )


llm = ChatGoogleGenerativeAI(
	model="gemini-3.8-flash",
	google_api_key=api_key,
	temperature=0.6,
	max_output_tokens=1024,
)

structured_llm = llm.with_structured_output(TicketAnalysis)

ticket_analysis_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """Analyze the customer support ticket using the provided structured output schema.
Classify the issue, assess urgency and sentiment, summarize the core problem,
identify the affected product or feature, and recommend the immediate next step.
Use only information supported by the ticket and keep the summary concise.""",
    ),
    ("human", "Customer support ticket:\n\n{ticket}"),
])


ticket_analysis_chain = ticket_analysis_prompt | structured_llm

def analyze_ticket(ticket: str) -> TicketAnalysis:
    return ticket_analysis_chain.invoke({"ticket": ticket})


if __name__ == "__main__":
    ticket = input("Enter your support query: ").strip()
    if ticket:
        analysis = analyze_ticket(ticket)
        print(analysis.model_dump_json(indent=2))



