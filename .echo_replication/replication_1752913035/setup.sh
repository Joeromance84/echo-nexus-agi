#!/bin/bash
# EchoNexus AGI Local Setup
echo "Setting up EchoNexus AGI locally..."

# Create virtual environment
python3 -m venv echo_nexus_env
source echo_nexus_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup_replication.py

# Start AGI
python echo_nexus_master.py

echo "EchoNexus AGI setup complete!"
