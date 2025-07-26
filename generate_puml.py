

import json

def generate_puml():
    """
    Reads the JSON data and generates a PlantUML file.
    """
    try:
        with open('memory_valid.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: memory_valid.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in memory_valid.json.")
        return

    puml_lines = ["@startuml"]
    
    # First, define all the entities
    for item in data:
        if item.get('type') == 'entity':
            name = item.get('name', 'Unnamed')
            # Sanitize the name for use as an alias
            alias = ''.join(e for e in name if e.isalnum() or e == '_')
            puml_lines.append(f'object "{name}" as {alias}')

    # Then, define all the relations
    for item in data:
        if item.get('type') == 'relation':
            from_node = item.get('from', 'Unnamed')
            to_node = item.get('to', 'Unnamed')
            relation_type = item.get('relationType', 'relates')
            
            from_alias = ''.join(e for e in from_node if e.isalnum() or e == '_')
            to_alias = ''.join(e for e in to_node if e.isalnum() or e == '_')

            puml_lines.append(f'{from_alias} --> {to_alias} : {relation_type}')

    puml_lines.append("@enduml")

    with open('knowledge_graph.puml', 'w') as f:
        f.write('\n'.join(puml_lines))

    print("Successfully generated knowledge_graph.puml")

if __name__ == "__main__":
    generate_puml()

