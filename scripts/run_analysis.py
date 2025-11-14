#!/usr/bin/env python3
"""
Automated Analysis Runner for Solar Challenge
Runs EDA and comparative analysis for all countries
"""

import os
import subprocess
import sys
from pathlib import Path

def run_notebook(notebook_path):
    """Execute a Jupyter notebook and save output"""
    try:
        print(f"🔬 Running analysis: {notebook_path}")
        
        # Convert notebook to script and execute
        cmd = [
            'jupyter', 'nbconvert', 
            '--to', 'notebook',
            '--execute',
            '--inplace',
            notebook_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Completed: {notebook_path}")
            return True
        else:
            print(f"❌ Failed: {notebook_path}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {notebook_path}: {e}")
        return False

def run_all_analyses():
    """Run all analysis notebooks in sequence"""
    notebooks = [
        'notebooks/benin_eda.ipynb',
        'notebooks/sierra_leone_eda.ipynb', 
        'notebooks/togo_eda.ipynb',
        'notebooks/country_comparison.ipynb'
    ]
    
    print("🔬 STARTING AUTOMATED ANALYSIS PIPELINE")
    print("=" * 50)
    
    # First, ensure data is processed
    print("📊 Step 1: Running data processing pipeline...")
    from data_pipeline import run_full_pipeline
    run_full_pipeline()
    
    # Run individual country analyses
    print("\n📈 Step 2: Running country EDA analyses...")
    for notebook in notebooks[:3]:  # First three are country EDAs
        success = run_notebook(notebook)
        if not success:
            print(f"⚠️  Skipping remaining analyses due to failure in {notebook}")
            return False
    
    # Run comparative analysis
    print("\n🏆 Step 3: Running comparative analysis...")
    success = run_notebook(notebooks[3])
    
    if success:
        print("\n🎉 ALL ANALYSES COMPLETED SUCCESSFULLY!")
        print("📁 Check the notebooks/ directory for results")
        return True
    else:
        print("\n❌ ANALYSIS PIPELINE COMPLETED WITH ERRORS")
        return False

def generate_analysis_report():
    """Generate a summary report of the analysis"""
    print("\n" + "="*50)
    print("ANALYSIS EXECUTION SUMMARY")
    print("="*50)
    
    report = """
📊 Analysis Pipeline Complete

Generated Files:
├── data/benin_clean.csv          # Cleaned Benin data
├── data/sierra_leone_clean.csv   # Cleaned Sierra Leone data  
├── data/togo_clean.csv           # Cleaned Togo data
├── notebooks/benin_eda.ipynb     # Benin EDA with outputs
├── notebooks/sierra_leone_eda.ipynb # Sierra Leone EDA with outputs
├── notebooks/togo_eda.ipynb      # Togo EDA with outputs
└── notebooks/country_comparison.ipynb # Comparative analysis

Next Steps:
1. Review the analysis notebooks
2. Check results/country_rankings.csv for investment recommendations
3. Update strategy report based on findings
"""
    print(report)

if __name__ == "__main__":
    success = run_all_analyses()
    if success:
        generate_analysis_report()
    else:
        sys.exit(1)