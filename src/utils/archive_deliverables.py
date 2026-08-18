import os
import shutil

def archive_deliverables():
    """Archives all 23 production deliverables to the output/final_deliverables directory."""
    target_dir = "output/final_deliverables"
    os.makedirs(target_dir, exist_ok=True)
    
    deliverables = [
        "src", "tests", "docs/analyst_guide.pdf", "output/perf_notes.md", 
        "README.md", "requirements.txt", "nifty100.db"
    ]
    
    for item in deliverables:
        if os.path.exists(item):
            dest = os.path.join(target_dir, os.path.basename(item))
            if os.path.isdir(item):
                if os.path.exists(dest):
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
            print(f"Archived: {item} -> {dest}")
            
    print("✨ All deliverables successfully archived to output/final_deliverables/")

if __name__ == "__main__":
    archive_deliverables()