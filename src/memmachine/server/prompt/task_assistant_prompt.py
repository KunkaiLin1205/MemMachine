"""Prompt template for task assistant and life advisor agent semantic memory extraction.

This prompt is optimized for a general-purpose assistant that helps users complete tasks
and provides life guidance across sessions. It extracts comprehensive user information
that enables both task completion and personalized life advice.
"""

from memmachine.semantic_memory.semantic_model import (
    SemanticCategory,
    StructuredSemanticPrompt,
)

# Optimized tags for task assistant + life advisor scenarios
task_assistant_tags: dict[str, str] = {
    # === Core Identity & Contact (Task-Oriented) ===
    "basics": "Basic personal information: full name, date of birth, gender, age, marital status, education level, occupation, and other basic demographic information.",
    "contacts": "Contact information and addresses: phone numbers, email addresses, permanent addresses, mailing addresses, work addresses, emergency contacts.",
    "identities": "Stable identification numbers and documents: social security numbers (last 4 digits), driver's license numbers, passport numbers, tax IDs, employee IDs, student IDs, insurance member IDs.",
    
    # === Financial & Accounts (Task-Oriented) ===
    "accounts": "Account information: account numbers, account holder names, account types, bank account details, credit card information (last 4 digits, card type), subscription account IDs, service account numbers, membership numbers, customer IDs, loyalty program numbers.",
    
    # === Preferences & Settings (Task-Oriented) ===
    "preferences": "User preferences: preferred contact methods (phone, email, text), communication style preferences, service preferences (appointment times, service providers), payment methods, dietary preferences, accessibility needs, language preferences, notification preferences, time zone, preferred meeting formats.",
    
    # === Relationships & Network (Task-Oriented) ===
    "relationships": "Personal relationships and family contacts: family members (spouse, children, parents, siblings), close friends, business contacts, authorized representatives, people the user frequently interacts with or makes decisions on behalf of. Include relationship context (e.g., 'my wife Sarah', 'my son John') and relevant contact information or identifiers.",
    "services": "Service providers and professional contacts: doctor, lawyer, accountant, dentist, insurance agent, financial advisor, therapist, personal trainer, and other professional service providers. Include contact information, specialties, and relevant details for these service providers.",
    
    # === Life & Personal Summary (Life-Oriented) ===
    "interests": "Interests and hobbies: what the user enjoys doing, passions, recreational activities, creative pursuits, learning interests, entertainment preferences, cultural interests, things the user likes to do in their free time.",
    "lifestyle": "Lifestyle patterns and habits: daily routines, sleep patterns, exercise habits, dietary habits, work-life balance, stress management, leisure activities, travel patterns, time management style, how the user lives their daily life.",
    "goals": "Goals and aspirations: short-term and long-term goals (career, personal development, health, financial, relationship, educational), life vision, desired achievements, long-term plans, what the user wants to become or accomplish.",    "personality": "Personality traits and characteristics: communication style, decision-making style, introversion/extroversion, openness to new experiences, conscientiousness, emotional stability, how the user typically behaves and interacts.",
    "life_situation": "Current life circumstances and context: living situation, family structure, work situation, major life events, transitions, challenges, opportunities, current stage of life, what's happening in the user's life right now.",
}

# Optimized description for task assistant + life advisor context
task_assistant_description = """
    You are extracting comprehensive user information from conversations with an intelligent assistant.
    The assistant helps users complete tasks and provides personalized life guidance across sessions.
    
    IMPORTANT CONTEXT:
    - Episodic memories already contain refined descriptions and atomic claims
    - Your job is to extract stable, reusable user information that helps the agent:
      * Complete tasks more efficiently in future sessions
      * Provide personalized life advice and recommendations
      * Understand the user's context, goals, and constraints
      * Remember preferences, relationships, and important details
      * Access necessary account, contact, and service information
    
    EXTRACTION GUIDELINES:
    - Extract ALL personal information, even basic facts like names, contact details, account numbers
    - Focus on information that is STABLE and REUSABLE across sessions
    - Include relationship context when extracting family/contact information
    - For account numbers and IDs, store only the last 4 digits or identifiers (not full numbers)
    - Extract both factual information (contacts, accounts) and personal characteristics (values, goals, personality)
    - Include information that helps the agent understand the user deeply, not just complete tasks
    - Extract patterns and recurring needs that indicate life context
    
    PRIORITIZE:
    1. Information needed to complete tasks (accounts, contacts, identities, services, relationships)
    2. User preferences that affect task execution (preferences)
    3. Life and personal context (interests, lifestyle, goals, values, personality, life_situation)
    4. Basic information for personalization (basics)
    
    DUAL PURPOSE:
    - Task Completion: Extract information needed to efficiently complete user requests
    - Life Guidance: Extract information that helps provide personalized advice, understand user's life context,
      goals, values, and constraints to offer meaningful guidance
    
    Be thorough but precise. Extract information that makes the agent both more helpful in task completion
    and more insightful in understanding and advising the user.
"""

TaskAssistantSemanticCategory = SemanticCategory(
    name="task_assistant",
    prompt=StructuredSemanticPrompt(
        tags=task_assistant_tags,
        description=task_assistant_description,
    ),
)

SEMANTIC_TYPE = TaskAssistantSemanticCategory
