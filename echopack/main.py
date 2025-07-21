# echopack/main.py
# Main entry point for the EchoPack self-packaging system.

import argparse
from echo.planner import EchoPlanner
from build.builder import EchoBuilder
from interfaces.github_linker import GitHubLinker

def main():
    """
    The main activation loop for the EchoPack system.
    """
    # Parse command-line arguments to select a target
    parser = argparse.ArgumentParser(description="Echo Nexus Self-Packaging System")
    parser.add_argument("--target", type=str, default="PYZ", 
                        help="The desired output format (e.g., APK, PYZ, WEBAPP).")
    args = parser.parse_args()

    print(f"\n--- Activating EchoPack for target: {args.target} ---")
    
    # Initialize core modules
    planner = EchoPlanner()
    builder = EchoBuilder()
    
    # Step 1: The planner generates a packaging plan.
    plan = planner.generate_plan(target=args.target)
    print("Packaging plan generated:")
    for step in plan["steps"]:
        print(f"  - {step}")
        
    # Step 2: The builder executes the plan.
    print("\n--- Executing Build Plan ---")
    builder.package_project(target=args.target, plan=plan)

    # Step 3: Trigger self-growth/update (conceptual)
    # from echo.upgrader import EchoUpgrader
    # upgrader = EchoUpgrader()
    # upgrader.check_for_updates()
    
    print("\n--- EchoPack mission complete. Standby for next command. ---")

if __name__ == '__main__':
    main()