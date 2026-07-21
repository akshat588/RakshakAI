from api.threat_intelligence import (
    reputation_engine,
    severity_engine,
    campaign_mapper,
    timeline_builder,
)

self.reputation_engine = reputation_engine
self.severity_engine = severity_engine
self.campaign_mapper = campaign_mapper
self.timeline_builder = timeline_builder

# ==========================================================
# Threat Intelligence Enrichment
# ==========================================================

reputation_result = {
    "found": False,
    "indicator": None,
    "indicator_type": None,
    "risk": "safe",
    "confidence": 0,
}

detected_type = investigation_result.get("detected_type")

indicator_mapping = {
    "url": investigation_result.get("url"),
    "email": investigation_result.get("email"),
    "upi": investigation_result.get("upi_id"),
    "domain": investigation_result.get("domain"),
    "ip": investigation_result.get("ip_address"),
}

indicator = indicator_mapping.get(detected_type)

if indicator:

    reputation_result = self.reputation_engine.check(
        indicator,
        detected_type,
    )

campaign_result = self.campaign_mapper.map_campaign(investigation_result.get("iocs", []))

severity_result = self.severity_engine.evaluate(
    analyzer_confidence=investigation_result.get(
        "confidence",
        0,
    ),
    reputation_confidence=reputation_result.get(
        "confidence",
        0,
    ),
    ioc_count=len(investigation_result.get("iocs", [])),
    mitre_count=len(investigation_result.get("mitre_attack", [])),
    malicious_analyzers=len(investigation_result.get("triggered_analyzers", [])),
)

timeline_result = self.timeline_builder.build(
    {
        "analyzers": investigation_result.get("analyzers", []),
        "reputation": reputation_result,
        "campaign": campaign_result,
        "severity": severity_result["severity"],
        "risk_score": severity_result["risk_score"],
    }
)

investigation_result["reputation"] = reputation_result
investigation_result["campaign"] = campaign_result
investigation_result["severity"] = severity_result["severity"]
investigation_result["risk_score"] = severity_result["risk_score"]
investigation_result["timeline"] = timeline_result
