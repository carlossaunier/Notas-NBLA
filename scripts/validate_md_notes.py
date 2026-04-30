import os
import re

def validate_notes():
    base_dir = '/Users/carlossaunier/NBLA/data/notas'
    book_dirs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
    
    report = []
    total_notes = 0
    total_files = 0
    
    for book_dir in book_dirs:
        dir_path = os.path.join(base_dir, book_dir)
        md_files = [f for f in os.listdir(dir_path) if f.endswith('_notas.md')]
        
        if not md_files:
            report.append(f"[MISSING] No _notas.md found in {book_dir}")
            continue
            
        md_file = os.path.join(dir_path, md_files[0])
        total_files += 1
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
        except Exception as e:
            report.append(f"[ERROR] Could not read {md_file}: {e}")
            continue
            
        # Check for main title
        if not any(line.startswith('# ') for line in lines):
            report.append(f"[WARNING] No main title (#) found in {md_file}")
            
        # Check for note headers
        headers = [line for line in lines if line.startswith('###')]
        if not headers:
            report.append(f"[EMPTY?] No note headers (###) found in {md_file}")
        else:
            total_notes += len(headers)
            # Check for suspicious headers (too long, no spaces, etc)
            for h in headers:
                if len(h) > 100:
                    report.append(f"[LONG HEADER] In {md_file}: {h[:50]}...")
                # Check if it looks like a bible reference (at least one number)
                if not any(c.isdigit() for c in h):
                    report.append(f"[MALFORMED HEADER] In {md_file}: {h}")

    print(f"Validation complete.")
    print(f"Total books processed: {len(book_dirs)}")
    print(f"Total MD files found: {total_files}")
    print(f"Total note entries: {total_notes}")
    
    if report:
        print("\nIssues found:")
        for issue in report:
            print(f"- {issue}")
    else:
        print("\nNo major structural issues found in .md files.")

if __name__ == '__main__':
    validate_notes()
