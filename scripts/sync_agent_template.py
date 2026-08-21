#!/usr/bin/env python3
"""
sync_agent_template.py - AI Agent Template Sync and Initialization Tool

Cross-platform tool to deploy and synchronize Core AI Agent template assets.
Supports Linux, macOS, and Windows with strict exit codes (0 = Success, 1 = Failure).
"""

import sys
import os
import shutil
import json
import argparse
from pathlib import Path
from datetime import datetime

# Core skills list
CORE_SKILLS = [
    "architecture-decision-records",
    "requirements-to-spec",
    "self-audit-and-regression-prevention",
    "large-scale-code-refactoring",
    "release-review",
    "design-and-plan",
    "implementation-and-refactor",
    "testing-and-verification",
    "performance-tuning-and-caching",
    "template-generalization-and-audit"
]

def get_template_root() -> Path:
    """Returns the root directory of the template."""
    return Path(__file__).resolve().parent.parent

def run_self_diagnosis(template_root: Path, is_dry_run: bool = False) -> int:
    """Validates the integrity of the template itself."""
    print("========================================================")
    print("  [DIAGNOSIS] AI Agent Template Self-Diagnosis")
    print("========================================================")
    print(f"Template Root: {template_root}")
    print(f"Core Skills Count: {len(CORE_SKILLS)}")

    agents_dir = template_root / ".agents"
    config_file = agents_dir / "agent_config.json"
    agents_md = agents_dir / "AGENTS.md"
    readme_md = agents_dir / "README.md"
    root_readme = template_root / "README.md"
    adr_template = template_root / "docs" / "adr" / "0000_template.md"

    errors = []

    # Check Core Files
    for f in [config_file, agents_md, readme_md, root_readme, adr_template]:
        if not f.exists():
            errors.append(f"Missing core file: {f}")
        else:
            print(f"  [OK] Found {f.relative_to(template_root)}")

    # Validate JSON
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as jf:
                json.load(jf)
            print("  [OK] agent_config.json is valid JSON")
        except Exception as e:
            errors.append(f"agent_config.json JSON parse error: {e}")

    # Check Skills
    for s in CORE_SKILLS:
        skill_md = agents_dir / "skills" / s / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"Missing skill: {s}")
        else:
            print(f"  [OK] Skill '{s}' verified")

    if errors:
        print("\n[FAIL] Self-diagnosis failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("\n[PASS] All template assets validated successfully (exit 0).")
    return 0

def run_smoke_test(template_root: Path) -> int:
    """Performs a full deployment and verification smoke test in a temp directory."""
    print("========================================================")
    print("  [TEST] AI Agent Template Smoke Test (-Test)")
    print("========================================================")

    # 1. Run Self-Diagnosis
    diag_res = run_self_diagnosis(template_root)
    if diag_res != 0:
        return diag_res

    # 2. Test Init in temporary directory
    temp_test_dir = template_root / "_smoke_test_sandbox"
    try:
        if temp_test_dir.exists():
            shutil.rmtree(temp_test_dir)

        print(f"\n[Test 1/3] Deploying to sandbox: {temp_test_dir}")
        deploy_res = deploy_template(template_root, temp_test_dir, is_dry_run=False, force=True)
        if deploy_res != 0:
            print("[FAIL] Deploy to sandbox failed.")
            return 1

        # 3. Verify deployed files
        print("\n[Test 2/3] Verifying deployed structure...")
        deployed_agents = temp_test_dir / ".agents"
        if not (deployed_agents / "AGENTS.md").exists():
            print("[FAIL] Deployed AGENTS.md missing.")
            return 1
        if not (deployed_agents / "agent_config.json").exists():
            print("[FAIL] Deployed agent_config.json missing.")
            return 1

        # Check for hardcoded absolute paths in deployed files
        print("\n[Test 3/3] Checking for hardcoded absolute paths (file:///c:)...")
        found_abs_paths = []
        for root, _, files in os.walk(deployed_agents):
            for file in files:
                if file.endswith((".md", ".json")):
                    file_path = Path(root) / file
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "file:///c:" in content.lower():
                            found_abs_paths.append(str(file_path.relative_to(temp_test_dir)))

        if found_abs_paths:
            print(f"[FAIL] Hardcoded absolute paths found in: {found_abs_paths}")
            return 1
        else:
            print("  [OK] Zero hardcoded absolute paths found.")

        print("\n[PASS] Smoke test completed successfully (exit 0)!")
        return 0
    finally:
        if temp_test_dir.exists():
            shutil.rmtree(temp_test_dir)
        # Clean up any generated pycache directories
        for root, dirs, _ in os.walk(template_root):
            for d in dirs:
                if d == "__pycache__":
                    pycache_path = Path(root) / d
                    try:
                        shutil.rmtree(pycache_path)
                    except Exception:
                        pass

def deploy_template(template_root: Path, target_path: Path, is_dry_run: bool = False, force: bool = False) -> int:
    """Deploys Core assets to the target project directory."""
    print(f"[TARGET] Target Project: {target_path}")

    target_agents = target_path / ".agents"
    target_skills = target_agents / "skills"
    target_scripts = target_path / "scripts"
    target_docs = target_path / "docs" / "guides"

    # Backup existing .agents
    if target_agents.exists() and not force:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = target_path / f".agents.bak_{timestamp}"
        if is_dry_run:
            print(f"[DryRun] Backup existing .agents -> {backup_path}")
        else:
            shutil.copytree(target_agents, backup_path)
            print(f"[BACKUP] Backup created: {backup_path}")

    source_agents = template_root / ".agents"

    # 1. AGENTS.md & README.md & agent_config.json & DOMAIN.md.example
    core_files = ["AGENTS.md", "README.md", "agent_config.json", "DOMAIN.md.example"]
    for cf in core_files:
        src = source_agents / cf
        dst = target_agents / cf
        if src.exists():
            if is_dry_run:
                print(f"[DryRun] Deploy: {cf}")
            else:
                target_agents.mkdir(parents=True, exist_ok=True)
                if cf == "agent_config.json":
                    with open(src, "r", encoding="utf-8") as f:
                        cfg_content = f.read()
                    cfg_content = cfg_content.replace("{{PROJECT_NAME}}", target_path.name)
                    cfg_content = cfg_content.replace("{{config_path}}", ".agents/agent_config.json")
                    with open(dst, "w", encoding="utf-8") as f:
                        f.write(cfg_content)
                else:
                    shutil.copy2(src, dst)
                print(f"  + Deployed: .agents/{cf}")

    # 2. Deploy Core Skills (ignoring __pycache__)
    for skill in CORE_SKILLS:
        src_skill = source_agents / "skills" / skill
        dst_skill = target_skills / skill
        if src_skill.exists():
            if is_dry_run:
                print(f"[DryRun] Deploy Skill: {skill}")
            else:
                if dst_skill.exists():
                    shutil.rmtree(dst_skill)
                shutil.copytree(src_skill, dst_skill, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                print(f"  + Deployed Skill: {skill}")

    # 3. Deploy scripts (sync_agent_template.py and wrappers, ignoring pyc)
    src_scripts = template_root / "scripts"
    if src_scripts.exists():
        for script_file in src_scripts.glob("sync_agent_template.*"):
            if script_file.suffix == ".pyc":
                continue
            dst_script = target_scripts / script_file.name
            if is_dry_run:
                print(f"[DryRun] Deploy Script: {script_file.name}")
            else:
                target_scripts.mkdir(parents=True, exist_ok=True)
                shutil.copy2(script_file, dst_script)
                print(f"  + Deployed: scripts/{script_file.name}")

    # 4. Deploy Lifecycle Guide & ADR Template
    src_guide = template_root / "docs" / "guides" / "AGENT_TEMPLATE_LIFECYCLE.md"
    if src_guide.exists():
        dst_guide = target_docs / "AGENT_TEMPLATE_LIFECYCLE.md"
        if is_dry_run:
            print("[DryRun] Deploy Guide: AGENT_TEMPLATE_LIFECYCLE.md")
        else:
            target_docs.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_guide, dst_guide)
            print("  + Deployed: docs/guides/AGENT_TEMPLATE_LIFECYCLE.md")

    src_adr_tpl = template_root / "docs" / "adr" / "0000_template.md"
    if src_adr_tpl.exists():
        target_adr = target_path / "docs" / "adr"
        dst_adr_tpl = target_adr / "0000_template.md"
        if is_dry_run:
            print("[DryRun] Deploy ADR Template: docs/adr/0000_template.md")
        else:
            target_adr.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_adr_tpl, dst_adr_tpl)
            print("  + Deployed: docs/adr/0000_template.md")

    print("\n[SUCCESS] AI Agent template successfully deployed!")
    return 0

def main():
    parser = argparse.ArgumentParser(description="AI Agent Template Sync & Init Tool")
    parser.add_argument("-Init", "--init", action="store_true", help="Initialize template in target project")
    parser.add_argument("-TargetPath", "--target-path", type=str, default="", help="Target project root directory")
    parser.add_argument("-Test", "--test", action="store_true", help="Run automated smoke test")
    parser.add_argument("-DryRun", "--dry-run", action="store_true", help="Simulate execution without modifying files")
    parser.add_argument("-Force", "--force", action="store_true", help="Overwrite without creating backup")

    args = parser.parse_args()
    template_root = get_template_root()

    if args.test:
        sys.exit(run_smoke_test(template_root))

    if args.init:
        if not args.target_path:
            print("❌ [ERROR] -Init mode requires -TargetPath <dir>")
            sys.exit(1)
        target = Path(args.target_path).resolve()
        sys.exit(deploy_template(template_root, target, is_dry_run=args.dry_run, force=args.force))

    # Default: Self-Diagnosis
    sys.exit(run_self_diagnosis(template_root, is_dry_run=args.dry_run))

if __name__ == "__main__":
    main()
