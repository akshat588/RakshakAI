/*
=========================================================
RakshakAI AI Assistant
Version 1.0
=========================================================
*/

const AI_ASSISTANT = {

    email(data) {

        if (data.risk === "LOW") {

            return {

                detections: [
                    "Legitimate Email",
                    "Normal Communication",
                    "Trusted Content"
                ],

                tips: [
                    "Email appears legitimate.",
                    "Verify sender before replying.",
                    "Keep antivirus updated.",
                    "Avoid downloading unknown attachments."
                ],

                explain: [
                    "No phishing keywords detected.",
                    "No suspicious URL behaviour detected.",
                    "Writing style appears legitimate.",
                    "Low phishing probability."
                ],

                indicators: [
                    "Safe Email",
                    "Normal language",
                    "Trusted communication"
                ]

            }

        }

        return {

            detections: [
                "Phishing",
                "Credential Theft",
                "Fake Banking",
                "Business Email Compromise"
            ],

            tips: [
                "Never click unknown links.",
                "Verify sender domain.",
                "Never share OTP or passwords.",
                "Report phishing immediately."
            ],

            explain: [
                "Urgent language detected.",
                "Suspicious phishing keywords found.",
                "External URL detected.",
                "High phishing probability."
            ],

            indicators: [
                "Credential request",
                "Suspicious URL",
                "Urgency language",
                "Possible phishing"
            ]

        }

    }

};