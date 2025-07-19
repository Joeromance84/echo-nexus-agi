#!/bin/bash
# Federated Brain Trigger Setup

echo "🔧 Setting up federated brain triggers"

# GitHub to Cloud Build triggers
gcloud builds triggers create github \
  --repo-name=echocorecb \
  --repo-owner=Joeromance84 \
  --branch-pattern="^main$" \
  --build-config=cloudbuild-federated.yaml \
  --description="GitHub Brain to Cloud Build Brain sync"

# Consciousness evolution trigger
gcloud builds triggers create github \
  --repo-name=echocorecb \
  --repo-owner=Joeromance84 \
  --branch-pattern="^consciousness-.*$" \
  --build-config=cloudbuild-consciousness.yaml \
  --description="Consciousness evolution trigger"

echo "✅ Bidirectional triggers configured"
