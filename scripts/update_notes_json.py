import os
import json
import re

# Book map to match index.html logic
BOOK_MAP = {
    'gen': 'Génesis', 'gén': 'Génesis', 'génesis': 'Génesis', 'genesis': 'Génesis',
    'ex': 'Éxodo', 'éx': 'Éxodo', 'exo': 'Éxodo', 'exodo': 'Éxodo', 'éxodo': 'Éxodo',
    'lev': 'Levítico', 'levitico': 'Levítico', 'levítico': 'Levítico',
    'num': 'Números', 'núm': 'Números', 'numeros': 'Números', 'números': 'Números',
    'deu': 'Deuteronomio', 'deut': 'Deuteronomio', 'deuteronomio': 'Deuteronomio', 'dt': 'Deuteronomio',
    'jos': 'Josué', 'josue': 'Josué', 'josué': 'Josué',
    'jue': 'Jueces', 'juec': 'Jueces', 'jueces': 'Jueces',
    'rut': 'Rut', 'rt': 'Rut',
    '1 sam': '1 Samuel', '1sam': '1 Samuel', '1samuel': '1 Samuel',
    '2 sam': '2 Samuel', '2sam': '2 Samuel', '2samuel': '2 Samuel',
    '1 rey': '1 Reyes', '1rey': '1 Reyes', '1re': '1 Reyes', '1reyes': '1 Reyes',
    '2 rey': '2 Reyes', '2rey': '2 Reyes', '2re': '2 Reyes', '2reyes': '2 Reyes',
    '1 cr': '1 Crónicas', '1cr': '1 Crónicas', '1cro': '1 Crónicas', '1cronicas': '1 Crónicas', '1crónicas': '1 Crónicas',
    '2 cr': '2 Crónicas', '2cr': '2 Crónicas', '2cro': '2 Crónicas', '2cronicas': '2 Crónicas', '2crónicas': '2 Crónicas',
    'esd': 'Esdras', 'esdras': 'Esdras',
    'neh': 'Nehemías', 'nehemias': 'Nehemías', 'nehemías': 'Nehemías',
    'est': 'Ester', 'ester': 'Ester',
    'job': 'Job',
    'sal': 'Salmos', 'salm': 'Salmos', 'salmo': 'Salmos', 'salmos': 'Salmos', 'ps': 'Salmos',
    'pro': 'Proverbios', 'prov': 'Proverbios', 'proverbios': 'Proverbios', 'pr': 'Proverbios',
    'ecl': 'Eclesiastés', 'eclesiastes': 'Eclesiastés', 'eclesiastés': 'Eclesiastés',
    'cnt': 'Cantares', 'can': 'Cantares', 'cantares': 'Cantares',
    'is': 'Isaías', 'isa': 'Isaías', 'isaias': 'Isaías', 'isaías': 'Isaías',
    'jer': 'Jeremías', 'jeremias': 'Jeremías', 'jeremías': 'Jeremías',
    'lam': 'Lamentaciones', 'lamentaciones': 'Lamentaciones',
    'ez': 'Ezequiel', 'eze': 'Ezequiel', 'ezequiel': 'Ezequiel',
    'dn': 'Daniel', 'dan': 'Daniel', 'daniel': 'Daniel',
    'os': 'Oseas', 'oseas': 'Oseas',
    'jl': 'Joel', 'joel': 'Joel',
    'am': 'Amós', 'amos': 'Amós', 'amós': 'Amós',
    'ab': 'Abdías', 'abd': 'Abdías', 'abdias': 'Abdías', 'abdías': 'Abdías',
    'jon': 'Jonás', 'jonas': 'Jonás', 'jonás': 'Jonás',
    'mi': 'Miqueas', 'miq': 'Miqueas', 'miqueas': 'Miqueas',
    'nah': 'Nahum', 'nahum': 'Nahum',
    'hab': 'Habacuc', 'habacuc': 'Habacuc',
    'sof': 'Sofonías', 'sofonias': 'Sofonías', 'sofonías': 'Sofonías',
    'hag': 'Hageo', 'hageo': 'Hageo',
    'zac': 'Zacarías', 'zacarias': 'Zacarías', 'zacarías': 'Zacarías',
    'mal': 'Malaquías', 'malaquias': 'Malaquías', 'malaquías': 'Malaquías',
    'mt': 'Mateo', 'mat': 'Mateo', 'mateo': 'Mateo',
    'mr': 'Marcos', 'marc': 'Marcos', 'marcos': 'Marcos', 'mc': 'Marcos',
    'lc': 'Lucas', 'luc': 'Lucas', 'lucas': 'Lucas',
    'jn': 'Juan', 'juan': 'Juan',
    'hch': 'Hechos', 'hec': 'Hechos', 'hechos': 'Hechos',
    'ro': 'Romanos', 'rom': 'Romanos', 'romanos': 'Romanos',
    '1 cor': '1 Corintios', '1cor': '1 Corintios', '1co': '1 Corintios',
    '2 cor': '2 Corintios', '2cor': '2 Corintios', '2co': '2 Corintios',
    'ga': 'Gálatas', 'gal': 'Gálatas', 'galatas': 'Gálatas', 'gálatas': 'Gálatas',
    'ef': 'Efesios', 'efe': 'Efesios', 'efesios': 'Efesios',
    'fil': 'Filipenses', 'filip': 'Filipenses', 'filipenses': 'Filipenses',
    'col': 'Colosenses', 'colosenses': 'Colosenses',
    '1 tes': '1 Tesalonicenses', '1ts': '1 Tesalonicenses', '1tesalonicenses': '1 Tesalonicenses',
    '2 tes': '2 Tesalonicenses', '2ts': '2 Tesalonicenses', '2tesalonicenses': '2 Tesalonicenses',
    '1 tim': '1 Timoteo', '1tim': '1 Timoteo', '1timoteo': '1 Timoteo',
    '2 tim': '2 Timoteo', '2tim': '2 Timoteo', '2timoteo': '2 Timoteo',
    'tit': 'Tito', 'tito': 'Tito',
    'flm': 'Filemón', 'filemon': 'Filemón', 'filemón': 'Filemón',
    'heb': 'Hebreos', 'hebreos': 'Hebreos',
    'stgo': 'Santiago', 'sant': 'Santiago', 'santiago': 'Santiago',
    '1 ped': '1 Pedro', '1ped': '1 Pedro', '1pe': '1 Pedro',
    '2 ped': '2 Pedro', '2ped': '2 Pedro', '2pe': '2 Pedro',
    '1 jn': '1 Juan', '1jn': '1 Juan',
    '2 jn': '2 Juan', '2jn': '2 Juan',
    '3 jn': '3 Juan', '3jn': '3 Juan',
    'jud': 'Judas', 'judas': 'Judas',
    'ap': 'Apocalipsis', 'apo': 'Apocalipsis', 'apocalipsis': 'Apocalipsis', 'rev': 'Apocalipsis'
}

def normalize_ref(raw_header):
    # Match pattern: Book Chapter:Verse or Book Chapter
    match = re.search(r'((?:\d\s?)?[A-ZÁÉÍÓÚÑa-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚÑa-záéíóúñ]+)*)\.?\s+(\d+)(?::(\d+))?', raw_header)
    if not match:
        return raw_header.strip()
    
    book_raw = match.group(1).lower().replace('.', '').strip()
    chapter = match.group(2)
    verse = match.group(3)
    
    book_norm = BOOK_MAP.get(book_raw, book_raw.capitalize())
    
    if verse:
        return f"{book_norm} {chapter}:{verse}"
    else:
        return f"{book_norm} {chapter}"

def parse_md_file(file_path):
    notes = {}
    current_ref = None
    current_content = []
    
    # Navigation markers to remove
    nav_markers = [
        r'REGRESE A.*',
        r'Regrese a.*',
        r'Ir a.*'
    ]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            stripped_line = line.strip()
            
            if stripped_line.startswith('###'):
                # Save previous note if it exists
                if current_ref and current_content:
                    notes[current_ref] = "\n".join(current_content).strip()
                
                # Extract and normalize new reference
                raw_ref = stripped_line.replace('###', '').strip()
                current_ref = normalize_ref(raw_ref)
                current_content = []
            elif stripped_line == '---':
                continue
            elif stripped_line.startswith('# '): # Main title
                continue
            else:
                if current_ref:
                    # Filter out navigation markers
                    is_nav = False
                    for marker in nav_markers:
                        if re.search(marker, stripped_line, re.IGNORECASE):
                            is_nav = True
                            break
                    if not is_nav:
                        current_content.append(line.rstrip('\n'))
        
        # Save last note
        if current_ref and current_content:
            notes[current_ref] = "\n".join(current_content).strip()
            
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        
    return notes

def main():
    base_dir = '/Users/carlossaunier/NBLA/data/notas'
    output_file = '/Users/carlossaunier/NBLA/study-tool/final_theological_notes.json'
    
    all_notes = {}
    
    book_dirs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
    
    for book_dir in book_dirs:
        dir_path = os.path.join(base_dir, book_dir)
        md_files = [f for f in os.listdir(dir_path) if f.endswith('_notas.md')]
        
        if not md_files:
            continue
            
        md_file = os.path.join(dir_path, md_files[0])
        print(f"Processing {md_file}...")
        
        book_notes = parse_md_file(md_file)
        all_notes.update(book_notes)
        
    # Write to final JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_notes, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated {output_file} with {len(all_notes)} entries.")

if __name__ == "__main__":
    main()
