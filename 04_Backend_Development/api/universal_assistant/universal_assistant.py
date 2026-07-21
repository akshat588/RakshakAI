"reputation": investigation_result.get(
    "reputation",
    {}
),

"campaign": investigation_result.get(
    "campaign",
    {}
),

"severity": investigation_result.get(
    "severity",
    "safe",
),

"risk_score": investigation_result.get(
    "risk_score",
    0,
),

"timeline": investigation_result.get(
    "timeline",
    [],
),