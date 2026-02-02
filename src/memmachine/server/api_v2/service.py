"""API v2 service implementations."""

from dataclasses import dataclass

from fastapi import Request

from memmachine import MemMachine
from memmachine.common.api import MemoryType as MemoryTypeE
from memmachine.common.api.spec import (
    AddMemoriesSpec,
    AddMemoryResult,
    Episode,
    EpisodicSearchResult,
    ListMemoriesSpec,
    ListResult,
    ListResultContent,
    SearchMemoriesSpec,
    SearchResult,
    SearchResultContent,
    SemanticFeature,
)
from memmachine.common.episode_store.episode_model import EpisodeEntry


# Placeholder dependency injection function
async def get_memmachine(request: Request) -> MemMachine:
    """Get session data manager instance."""
    return request.app.state.mem_machine


@dataclass
class _SessionData:
    org_id: str
    project_id: str
    user_id: str | None = None
    role_id: str | None = None
    session_id_override: str | None = None

    @property
    def session_key(self) -> str:
        return f"{self.org_id}/{self.project_id}"

    @property
    def user_profile_id(self) -> str | None:
        return self.user_id

    @property
    def role_profile_id(self) -> str | None:
        return self.role_id

    @property
    def session_id(self) -> str | None:
        return self.session_id_override if self.session_id_override else self.session_key


def _extract_ids_from_messages(
    messages: list, project_id: str
) -> tuple[str | None, str | None, str | None]:
    """
    Extract user_id, role_id, and session_id from message metadata.
    
    If user_id is not provided in metadata, use project_id as user_id
    (assuming one user per project).
    """
    user_id: str | None = None
    role_id: str | None = None
    session_id: str | None = None

    # Extract from first message's metadata (assuming all messages have consistent metadata)
    if messages and hasattr(messages[0], "metadata") and messages[0].metadata:
        metadata = messages[0].metadata
        user_id = metadata.get("user_id")
        role_id = metadata.get("role_id")
        session_id = metadata.get("session_id")

    # If user_id is not provided, use project_id as user_id (one user per project)
    if user_id is None or user_id == "":
        user_id = project_id

    return user_id, role_id, session_id


async def _add_messages_to(
    target_memories: list[MemoryTypeE],
    spec: AddMemoriesSpec,
    memmachine: MemMachine,
) -> list[AddMemoryResult]:
    # Extract user_id, role_id, session_id from message metadata
    # If user_id is not provided, use project_id as user_id (one user per project)
    user_id, role_id, session_id = _extract_ids_from_messages(spec.messages, spec.project_id)

    episodes: list[EpisodeEntry] = [
        EpisodeEntry(
            content=message.content,
            producer_id=message.producer,
            produced_for_id=message.produced_for,
            producer_role=message.role,
            created_at=message.timestamp,
            metadata=message.metadata,
            episode_type=message.episode_type,
        )
        for message in spec.messages
    ]

    episode_ids = await memmachine.add_episodes(
        session_data=_SessionData(
            org_id=spec.org_id,
            project_id=spec.project_id,
            user_id=user_id,
            role_id=role_id,
            session_id_override=session_id,
        ),
        episode_entries=episodes,
        target_memories=target_memories,
    )
    return [AddMemoryResult(uid=e_id) for e_id in episode_ids]


async def _search_target_memories(
    target_memories: list[MemoryTypeE],
    spec: SearchMemoriesSpec,
    memmachine: MemMachine,
) -> SearchResult:
    # For search, use project_id as user_id (one user per project)
    # This ensures semantic memory search targets the correct user profile
    user_id: str | None = spec.project_id
    role_id: str | None = None
    session_id: str | None = None

    results = await memmachine.query_search(
        session_data=_SessionData(
            org_id=spec.org_id,
            project_id=spec.project_id,
            user_id=user_id,
            role_id=role_id,
            session_id_override=session_id,
        ),
        query=spec.query,
        target_memories=target_memories,
        search_filter=spec.filter,
        limit=spec.top_k,
        score_threshold=spec.score_threshold
        if spec.score_threshold is not None
        else -float("inf"),
    )
    content = SearchResultContent(
        episodic_memory=None,
        semantic_memory=None,
    )
    if results.episodic_memory is not None:
        content.episodic_memory = EpisodicSearchResult(
            **results.episodic_memory.model_dump(mode="json")
        )
    if results.semantic_memory is not None:
        content.semantic_memory = [
            SemanticFeature(**f.model_dump(mode="json"))
            for f in results.semantic_memory
        ]
    return SearchResult(
        status=0,
        content=content,
    )


async def _list_target_memories(
    target_memories: list[MemoryTypeE],
    spec: ListMemoriesSpec,
    memmachine: MemMachine,
) -> ListResult:
    # For list, use project_id as user_id (one user per project)
    # This ensures semantic memory list targets the correct user profile
    user_id: str | None = spec.project_id
    role_id: str | None = None
    session_id: str | None = None

    results = await memmachine.list_search(
        session_data=_SessionData(
            org_id=spec.org_id,
            project_id=spec.project_id,
            user_id=user_id,
            role_id=role_id,
            session_id_override=session_id,
        ),
        target_memories=target_memories,
        search_filter=spec.filter,
        page_size=spec.page_size,
        page_num=spec.page_num,
    )

    content = ListResultContent(
        episodic_memory=None,
        semantic_memory=None,
    )
    if results.episodic_memory is not None:
        content.episodic_memory = [
            Episode(**e.model_dump(mode="json")) for e in results.episodic_memory
        ]
    if results.semantic_memory is not None:
        content.semantic_memory = [
            SemanticFeature(**f.model_dump(mode="json"))
            for f in results.semantic_memory
        ]

    return ListResult(
        status=0,
        content=content,
    )
