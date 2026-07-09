const AI_EXPLANATIONS = {

    email: {

        "Phishing Email": {

            detections: [
                "Credential Theft",
                "Fake Banking",
                "Urgent Login Request",
                "Brand Impersonation",
                "Phishing Attempt"
            ],

            tips: [
                "Verify sender domain.",
                "Never click unknown links.",
                "Never share OTP.",
                "Report phishing emails.",
                "Check attachments carefully."
            ],

            recommendation:
                "This email appears malicious. Avoid clicking links or downloading attachments.",

            explanation: [
                "Suspicious language detected.",
                "Credential request identified.",
                "Urgency score increased.",
                "ML confidence will be displayed dynamically."
            ]

        },

        "Legitimate Email": {

            detections: [
                "Normal Communication",
                "Trusted Language",
                "No Credential Request",
                "Safe Content",
                "Verified Structure"
            ],

            tips: [
                "Always verify attachments.",
                "Keep antivirus updated.",
                "Check sender if unsure."
            ],

            recommendation:
                "This email appears legitimate.",

            explanation: [
                "No phishing keywords detected.",
                "Safe communication pattern.",
                "Low phishing probability."
            ]

        }

    }

};