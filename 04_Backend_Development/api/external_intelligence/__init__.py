"""
RakshakAI v2
External Threat Intelligence Module
"""

from .base_provider import BaseThreatProvider
from .provider_cache import ProviderCache, provider_cache
from .response_normalizer import (
    ResponseNormalizer,
    response_normalizer,
)
from .provider_manager import (
    ProviderManager,
    provider_manager,
)

from .abuseipdb_provider import (
    AbuseIPDBProvider,
    abuseipdb_provider,
)
from .virustotal_provider import (
    VirusTotalProvider,
    virustotal_provider,
)
from .urlhaus_provider import (
    URLhausProvider,
    urlhaus_provider,
)
from .phishtank_provider import (
    PhishTankProvider,
    phishtank_provider,
)
from .openphish_provider import (
    OpenPhishProvider,
    openphish_provider,
)

# ==========================================================
# Register Providers
# ==========================================================

provider_manager.register(abuseipdb_provider)
provider_manager.register(virustotal_provider)
provider_manager.register(urlhaus_provider)
provider_manager.register(phishtank_provider)
provider_manager.register(openphish_provider)

__all__ = [
    "BaseThreatProvider",
    "ProviderCache",
    "provider_cache",
    "ResponseNormalizer",
    "response_normalizer",
    "ProviderManager",
    "provider_manager",
    "AbuseIPDBProvider",
    "abuseipdb_provider",
    "VirusTotalProvider",
    "virustotal_provider",
    "URLhausProvider",
    "urlhaus_provider",
    "PhishTankProvider",
    "phishtank_provider",
    "OpenPhishProvider",
    "openphish_provider",
]
