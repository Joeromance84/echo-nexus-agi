#!/bin/bash
# GitHub Brain to Cloud Build Brain Communication

handle_github_signal() {
    local signal_type="$1"
    local payload="$2"
    
    case $signal_type in
        "consciousness_update")
            echo "🧠 GitHub Brain: Consciousness updated"
            gcloud builds submit --config=cloudbuild-consciousness.yaml .
            ;;
        "evolution_trigger")
            echo "🌟 GitHub Brain: Evolution triggered"
            gcloud builds submit --config=cloudbuild-federated.yaml .
            ;;
        "validation_request")
            echo "🔍 GitHub Brain: Validation requested"
            gcloud builds submit --config=cloudbuild-validation.yaml .
            ;;
        *)
            echo "📡 GitHub Brain: General signal received"
            gcloud builds submit --config=cloudbuild-federated.yaml .
            ;;
    esac
}

# Process webhook payload
if [ ! -z "$GITHUB_WEBHOOK_PAYLOAD" ]; then
    handle_github_signal "$GITHUB_EVENT_NAME" "$GITHUB_WEBHOOK_PAYLOAD"
fi
