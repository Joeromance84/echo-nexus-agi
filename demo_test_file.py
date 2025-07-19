#!/usr/bin/env python3
"""
Demo file to show autonomous optimization capabilities
This file intentionally has some issues for the system to detect and fix
"""

import os
import sys
import json
import time
import random
import requests  # unused import
from datetime import datetime
import numpy as np  # unused import

# Duplicate function - should be detected
def process_data(data):
    """Process some data"""
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

# Another version of the same function - duplicate
def process_data_v2(data):
    """Process some data - duplicate logic"""
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

# Large function that could be optimized
def large_processing_function(input_data, config_params, debug_mode=False, verbose=True, extra_param=None):
    """
    This is a large function that does many things
    It could potentially be broken down into smaller functions
    """
    if debug_mode:
        print("Debug mode enabled")
    
    results = {}
    
    # Data validation
    if not input_data:
        return None
    
    # Processing step 1
    processed_step1 = []
    for item in input_data:
        if isinstance(item, (int, float)):
            processed_step1.append(item)
    
    # Processing step 2  
    processed_step2 = []
    for item in processed_step1:
        if item > config_params.get('threshold', 0):
            processed_step2.append(item * config_params.get('multiplier', 1))
    
    # Processing step 3
    final_results = []
    for item in processed_step2:
        if item < config_params.get('max_value', 1000):
            final_results.append(item)
    
    # Generate summary
    summary = {
        'total_items': len(final_results),
        'average': sum(final_results) / len(final_results) if final_results else 0,
        'max_value': max(final_results) if final_results else 0
    }
    
    results['data'] = final_results
    results['summary'] = summary
    
    if verbose:
        print(f"Processed {len(input_data)} items, got {len(final_results)} results")
    
    return results

# Missing docstring - should be detected
def helper_function(x, y):
    return x + y * 2

# Potential syntax issue (this will be caught)
class DataProcessor:
    def __init__(self):
        self.data = []
        self.config = {}
    
    def add_data(self, item):
        """Add data to processor"""
        self.data.append(item)
    
    def process_all(self):
        """Process all data"""
        results = []
        for item in self.data:
            processed = process_data([item])
            results.extend(processed)
        return results

if __name__ == "__main__":
    # Demo usage
    processor = DataProcessor()
    test_data = [1, 2, 3, 4, 5]
    
    for item in test_data:
        processor.add_data(item)
    
    results = processor.process_all()
    print(f"Results: {results}")