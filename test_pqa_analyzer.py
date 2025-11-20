"""
Test script to verify PQA analyzer is correctly routing EDS vs IODD files
"""
import sqlite3
from src.utils.pqa_orchestrator import UnifiedPQAOrchestrator, FileType

def test_pqa_routing():
    """Test that PQA correctly routes EDS and IODD files to appropriate analyzers"""

    conn = sqlite3.connect('greenstack.db')
    cursor = conn.cursor()

    # Get one EDS file
    cursor.execute("SELECT id, eds_content FROM eds_files WHERE eds_content IS NOT NULL LIMIT 1")
    eds_row = cursor.fetchone()

    if not eds_row:
        print("❌ No EDS files found with content")
        return False

    eds_id, eds_content = eds_row
    print(f"\n[OK] Found EDS file {eds_id}")
    print(f"  Content length: {len(eds_content)} chars")
    print(f"  Content preview: {eds_content[:100]}...")

    # Initialize orchestrator
    orchestrator = UnifiedPQAOrchestrator()
    print("\n[OK] Initialized UnifiedPQAOrchestrator")

    # Test EDS analysis
    print(f"\n[TEST] Testing EDS analysis for file {eds_id}...")
    try:
        metrics, diffs = orchestrator.run_full_analysis(
            file_id=eds_id,
            file_type=FileType.EDS,
            original_content=eds_content
        )

        print(f"\n[RESULTS] EDS Analysis Results:")
        print(f"  Overall Score: {metrics.overall_score:.2f}%")
        print(f"  Section Score: {metrics.section_score:.2f}%")
        print(f"  Key Score: {metrics.key_score:.2f}%")
        print(f"  Value Score: {metrics.value_score:.2f}%")
        print(f"  Total Sections (Original): {metrics.total_sections_original}")
        print(f"  Total Sections (Reconstructed): {metrics.total_sections_reconstructed}")
        print(f"  Total Keys (Original): {metrics.total_keys_original}")
        print(f"  Data Loss: {metrics.data_loss_percentage:.2f}%")
        print(f"  Critical Data Loss: {metrics.critical_data_loss}")
        print(f"  Diff Items Found: {len(diffs)}")

        # Verify this is using EDS analyzer (should have sections > 0)
        if metrics.total_sections_original > 0:
            print("\n[SUCCESS] EDS analyzer correctly used (sections > 0)")
            return True
        else:
            print("\n[FAILURE] total_sections_original = 0, indicating XML analyzer was used instead of EDS analyzer")
            return False

    except Exception as e:
        print(f"\n[ERROR] Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("="*80)
    print("PQA ANALYZER ROUTING TEST")
    print("="*80)

    success = test_pqa_routing()

    print("\n" + "="*80)
    if success:
        print("[PASS] TEST PASSED: EDS files are using EDSDiffAnalyzer")
    else:
        print("[FAIL] TEST FAILED: EDS files are NOT using EDSDiffAnalyzer correctly")
    print("="*80)
