#!/usr/bin/env python3
"""Verify all finding files have valid YAML frontmatter with required fields."""

import yaml
import sys
from pathlib import Path

FINDINGS_DIR = Path(__file__).parent / "base12-base60-laboratory" / "docs" / "findings"
REQUIRED_FIELDS = ["status", "version"]
VALID_STATUSES = {"proven", "conjecture", "open", "refuted"}

def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file."""
    content = filepath.read_text()
    if not content.startswith("---"):
        return None, "Missing frontmatter delimiter (---)"
    
    try:
        # Find the closing ---
        parts = content.split("---", 2)
        if len(parts) < 3:
            return None, "Incomplete frontmatter (missing closing ---)"
        
        frontmatter_str = parts[1].strip()
        frontmatter = yaml.safe_load(frontmatter_str)
        
        if frontmatter is None:
            return None, "Empty frontmatter"
        
        return frontmatter, None
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"

def verify_file(filepath):
    """Verify a single finding file."""
    frontmatter, error = parse_frontmatter(filepath)
    if error:
        return False, [error]
    
    errors = []
    
    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")
    
    # Validate status
    if "status" in frontmatter:
        status = frontmatter["status"]
        if status not in VALID_STATUSES:
            errors.append(f"Invalid status '{status}'; must be one of {VALID_STATUSES}")
    
    # Validate version format (MAJOR.MINOR.PATCH)
    if "version" in frontmatter:
        version = frontmatter["version"]
        if not isinstance(version, str):
            errors.append(f"Version must be a string, got {type(version).__name__}")
        else:
            parts = version.split(".")
            if len(parts) != 3:
                errors.append(f"Version '{version}' must be MAJOR.MINOR.PATCH format")
            else:
                try:
                    for part in parts:
                        int(part)
                except ValueError:
                    errors.append(f"Version '{version}' parts must be integers")
    
    return len(errors) == 0, errors

def main():
    md_files = sorted(FINDINGS_DIR.glob("*.md"))
    # Exclude CHANGELOG.md from finding file checks
    finding_files = [f for f in md_files if f.name != "CHANGELOG.md"]
    
    print(f"Verifying {len(finding_files)} finding files in {FINDINGS_DIR}")
    print("=" * 60)
    
    all_passed = True
    results = {}
    
    for filepath in finding_files:
        passed, errors = verify_file(filepath)
        results[filepath.name] = (passed, errors)
        
        if passed:
            frontmatter, _ = parse_frontmatter(filepath)
            status = frontmatter.get("status", "?")
            version = frontmatter.get("version", "?")
            print(f"✓ {filepath.name:<40} status={status:<10} version={version}")
        else:
            all_passed = False
            print(f"✗ {filepath.name:<40} FAILED")
            for error in errors:
                print(f"    - {error}")
    
    print("=" * 60)
    
    # Also verify CHANGELOG.md exists
    changelog = FINDINGS_DIR / "CHANGELOG.md"
    if changelog.exists():
        print(f"✓ CHANGELOG.md exists")
    else:
        print(f"✗ CHANGELOG.md MISSING")
        all_passed = False
    
    # Summary
    passed_count = sum(1 for _, (p, _) in results.items() if p)
    print(f"\nSummary: {passed_count}/{len(finding_files)} finding files passed")
    
    if all_passed:
        print("\n✓ ALL VERIFICATIONS PASSED")
        return 0
    else:
        print("\n✗ SOME VERIFICATIONS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())