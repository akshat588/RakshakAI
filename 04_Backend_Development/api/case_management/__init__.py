"""
RakshakAI v2
Case Management Module
"""

from .investigation_store import (
    InvestigationStore,
    investigation_store,
)
from .history_manager import (
    HistoryManager,
    history_manager,
)
from .case_manager import (
    CaseManager,
    case_manager,
)
from .search_engine import (
    SearchEngine,
    search_engine,
)
from .filters import (
    CaseFilters,
    case_filters,
)
from .case_statistics import (
    CaseStatistics,
    case_statistics,
)
from .bookmarks import (
    Bookmarks,
    bookmarks,
)
from .tags import (
    Tags,
    tags,
)
from .notes import (
    Notes,
    notes,
)

__all__ = [
    "InvestigationStore",
    "investigation_store",
    "HistoryManager",
    "history_manager",
    "CaseManager",
    "case_manager",
    "SearchEngine",
    "search_engine",
    "CaseFilters",
    "case_filters",
    "CaseStatistics",
    "case_statistics",
    "Bookmarks",
    "bookmarks",
    "Tags",
    "tags",
    "Notes",
    "notes",
]
