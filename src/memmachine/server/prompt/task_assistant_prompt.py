"""Prompt template for task-oriented structured facts semantic memory extraction.

This prompt focuses on extracting stable, structured facts needed for task completion:
contact information, account details, identities, preferences, relationships, and services.
These facts are typically listed at the beginning of a session for quick reference.
"""

from memmachine.semantic_memory.semantic_model import (
    SemanticCategory,
    StructuredSemanticPrompt,
)

# Task-oriented structured facts tags
task_assistant_tags: dict[str, str] = {
    # === Core Identity & Contact ===
    "basics": "Basic personal information: full name, date of birth, gender, age, marital status, education level, occupation, and other basic demographic information.",
    "contacts": "Contact information and addresses: phone numbers, email addresses, permanent addresses, mailing addresses, work addresses, emergency contacts.",
    "identities": "Stable identification numbers and documents: social security numbers (last 4 digits), driver's license numbers, passport numbers, tax IDs, employee IDs, student IDs, insurance member IDs.",
    
    # === Financial & Accounts ===
    "accounts": "Account information: account numbers, account holder names, account types, bank account details, credit card information (last 4 digits, card type), subscription account IDs, service account numbers, membership numbers, customer IDs, loyalty program numbers.",
    
    # === Preferences & Settings ===
    "preferences": "User preferences: preferred contact methods (phone, email, text), communication style preferences, service preferences (appointment times, service providers), payment methods, dietary preferences, accessibility needs, language preferences, notification preferences, time zone, preferred meeting formats.",
    
    # === Relationships & Network ===
    "relationships": "Personal relationships and family contacts: family members (spouse, children, parents, siblings), close friends, business contacts, authorized representatives, people the user frequently interacts with or makes decisions on behalf of. Include relationship context (e.g., 'my wife Sarah', 'my son John') and relevant contact information or identifiers.",
    "services": "Service providers and professional contacts: doctor, lawyer, accountant, dentist, insurance agent, financial advisor, therapist, personal trainer, and other professional service providers. Include contact information, specialties, and relevant details for these service providers.",
}

# Optimized description for task-oriented structured facts
task_assistant_description = """
    You are extracting structured, factual user information from conversations with a task-oriented assistant.
    This information is used to efficiently complete user requests and is typically referenced at the start of sessions.
    
    IMPORTANT CONTEXT:
    - Episodic memories already contain refined descriptions and atomic claims, including all historical events and temporary states
    - Semantic memory is for STABLE, REUSABLE user information that persists across sessions
    - Your job is to extract structured facts that help the agent:
      * Quickly access contact information, account details, and identities
      * Remember user preferences for service interactions
      * Access relationship and service provider information
      * Complete tasks efficiently without asking for repeated information
    
    EXTRACTION GUIDELINES:
    - Extract ALL structured facts, even basic ones like names, contact details, account numbers
    - Focus on information that is STABLE and REUSABLE across sessions
    - Use clear, concise feature names that directly describe the fact (e.g., "FULL NAME", "EMAIL", "PHONE NUMBER", "BANK ACCOUNT LAST4")
    - For account numbers and IDs, store only the last 4 digits or identifiers (not full numbers)
    - Include relationship context when extracting family/contact information
    - Extract service provider information with contact details and specialties
    
    FEATURE NAMING GUIDELINES:
    - Use descriptive, specific feature names that clearly identify the information type
    - Use UPPERCASE letters with SPACES between words (e.g., "PHONE NUMBER", "EMAIL ADDRESS")
    - Be concise but clear - use full words, not abbreviations
    - Examples of good feature names:
      * "FULL NAME" (not "NAME" or "USER NAME")
      * "EMAIL" or "PRIMARY EMAIL" (not "CONTACT EMAIL")
      * "PHONE NUMBER" or "MOBILE PHONE" (not "PHONE" or "PHONE_NUMBER")
      * "BANK ACCOUNT LAST4" (not "ACCOUNT" or "BANK")
      * "CREDIT CARD LAST4" (not "CARD" or "PAYMENT METHOD")
      * "EMERGENCY CONTACT NAME" (not "EMERGENCY" or "CONTACT")
      * "PREFERRED PAYMENT METHOD" (not "PAYMENT" or "PREFERENCE")
      * "TIMEZONE" (not "TZ" or "TIME ZONE")
      * "DATE OF BIRTH" (not "DOB" or "BIRTHDATE")
      * "HOME ADDRESS" (not "ADDRESS" or "HOME")
    - Avoid generic names like "INFO", "DATA", "DETAIL" - be specific
    - For relationships: use format like "SPOUSE NAME", "CHILD NAME", "PARENT NAME"
    - For services: use format like "DOCTOR NAME", "LAWYER CONTACT", "ACCOUNTANT EMAIL"
    
    DO NOT EXTRACT (These belong in episodic memory, not semantic memory):
    - Historical events or past actions (e.g., "booked a flight on 2026-01-23", "visited Paris last summer")
    - Temporary states or pending actions (e.g., "flight_booking_pending", "waiting for payment")
    - One-time transactions or specific occurrences (e.g., "made a purchase", "called customer service")
    - Time-specific information that will become outdated (e.g., "currently traveling", "has a meeting tomorrow")
    - Travel history, booking history, transaction history, or any event-based information
    - Temporary preferences or context-dependent choices (e.g., "wants pizza today" vs. stable "prefers Italian food")
    
    ONLY EXTRACT STABLE STRUCTURED FACTS:
    - Permanent contact information (phone, email, addresses)
    - Stable account information (account numbers, IDs - last 4 digits only)
    - Long-term preferences (communication methods, service preferences, payment methods)
    - Relationship information that remains stable (family members, close contacts)
    - Service provider relationships with contact information
    
    PRIORITIZE:
    1. Contact information needed for task completion (contacts, basics)
    2. Account and identity information (accounts, identities)
    3. User preferences that affect task execution (preferences)
    4. Relationship and service provider information (relationships, services)
    
    Be precise and structured. Extract facts that can be quickly referenced at the start of sessions
    to complete tasks efficiently. Remember: if it's a one-time event or temporary state,
    it belongs in episodic memory, not semantic memory.
"""

TaskAssistantSemanticCategory = SemanticCategory(
    name="profile",
    prompt=StructuredSemanticPrompt(
        tags=task_assistant_tags,
        description=task_assistant_description,
    ),
)

SEMANTIC_TYPE = TaskAssistantSemanticCategory
