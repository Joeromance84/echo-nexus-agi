#!/usr/bin/env python3
"""
Test Document Learning App Startup
"""
import sys
import traceback

def test_app_startup():
    try:
        print("Testing Document Learning App startup...")
        
        # Test imports
        print("1. Testing imports...")
        import streamlit as st
        print("   ✅ streamlit imported")
        
        import document_learning_app
        print("   ✅ document_learning_app imported")
        
        # Test processor creation
        print("2. Testing processor creation...")
        processor = document_learning_app.DocumentLearningProcessor()
        print("   ✅ DocumentLearningProcessor created")
        
        # Test database
        print("3. Testing database...")
        if hasattr(processor, 'database'):
            print(f"   ✅ Database loaded with {len(processor.database.get('documents', {}))} documents")
        
        print("4. All tests passed - app should work!")
        return True
        
    except Exception as e:
        print(f"❌ Error during startup: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app_startup()
    sys.exit(0 if success else 1)