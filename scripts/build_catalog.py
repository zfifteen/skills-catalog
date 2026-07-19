#!/usr/bin/env python3
import os
import shutil
import json
import re
from pathlib import Path

def find_skill_files(base_dirs):
    skill_files = []
    for base in base_dirs:
        path = Path(base).expanduser()
        if path.exists():
            for p in path.rglob('SKILL.md'):
                skill_files.append(p)
    return skill_files

def parse_skill_metadata(skill_md_path):
    metadata = {
        'id': skill_md_path.parent.name,
        'name': skill_md_path.parent.name.replace('-', ' ').title(),
        'description': '',
        'category': 'Uncategorized'
    }
    
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            yaml_match = re.match(r'^-{3}\s*\n(.*?)\n-{3}', content, re.DOTALL)
            if yaml_match:
                frontmatter = yaml_match.group(1)
                
                # Extract short-description if present
                short_desc_match = re.search(r'^short-description:\s*["\']?(.*?)["\']?$', frontmatter, re.MULTILINE)
                if short_desc_match:
                    metadata['description'] = short_desc_match.group(1).strip()
                
                # Try to extract multiline description (> or >- or |)
                if not metadata['description']:
                    desc_match = re.search(r'^description:\s*(?:>|>-|\|)\s*\n(.*?)(?=\n[a-z-]+:|\Z)', frontmatter, re.DOTALL | re.MULTILINE | re.IGNORECASE)
                    if desc_match:
                        metadata['description'] = desc_match.group(1).strip().replace('\n', ' ')
                        metadata['description'] = re.sub(r'\s+', ' ', metadata['description'])
                    else:
                        # try single line description
                        single_desc = re.search(r'^description:\s*["\']?(.*?)["\']?$', frontmatter, re.MULTILINE | re.IGNORECASE)
                        if single_desc:
                            val = single_desc.group(1).strip()
                            if val not in ('>', '>-', '|'):
                                metadata['description'] = val

                # Extract other fields
                for line in frontmatter.splitlines():
                    if ':' in line:
                        key, val = line.split(':', 1)
                        key = key.strip().lower()
                        val = val.strip().strip("'\"")
                        if key in ('name', 'title') and val not in ('>', '>-', '|'):
                            metadata['name'] = val
                        elif key == 'category' and val not in ('>', '>-', '|'):
                            metadata['category'] = val
                            
            # Fallback if no description found in frontmatter: derive it from content
            if not metadata['description']:
                # Analyze skill by reading the first paragraph after YAML
                body = content[yaml_match.end():] if yaml_match else content
                paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and not p.strip().startswith('#')]
                if paragraphs:
                    metadata['description'] = (paragraphs[0][:150] + '...') if len(paragraphs[0]) > 150 else paragraphs[0]
                else:
                    metadata['description'] = "Provides functionality related to " + metadata['name']
                            
    except Exception as e:
        print(f"Error parsing {skill_md_path}: {e}")
        
    return metadata

def generate_data_js(skills, output_path):
    js_content = f"const skillsData = {json.dumps(skills, indent=2)};\n"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

def main():
    base_dirs = ['~/.grok', '~/.gemini', '~/.codex']
    project_dir = Path(__file__).parent.parent
    local_skills_dir = project_dir / 'skills'
    
    print("Finding skill files...")
    skill_files = find_skill_files(base_dirs)
    
    unique_skills = {}
    for sf in skill_files:
        skill_id = sf.parent.name
        if skill_id not in unique_skills:
            unique_skills[skill_id] = sf
    
    skills_data = []
    
    for skill_id, sf in unique_skills.items():
        metadata = parse_skill_metadata(sf)
        metadata['localPath'] = f"skills/{skill_id}"
        skills_data.append(metadata)
            
    data_js_path = project_dir / 'data.js'
    generate_data_js(skills_data, data_js_path)
    print(f"Successfully processed {len(skills_data)} skills and regenerated data.js")

if __name__ == '__main__':
    main()
