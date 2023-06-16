import pandas as pd
import json


if __name__ == '__main__':
    input_files = ['profiles/gdoc_csv/source.csv', 'profiles/gdoc_csv/tissue_types.csv', 'profiles/gdoc_csv/pathological_alterations.csv']
    cols = ['CODE', 'NAME', 'PARENT', 'COLOR', 'COMMENT']
    layer_names = ['Source', 'Tissue Type', 'Pathological Alteration']

    layer_nodes = []

    for layer_idx, file in enumerate(input_files):
        df = pd.read_csv(file)
        df['COMMENT'] = df['COMMENT'].fillna('')
        df['CODE'] = df['CODE'].fillna('')

        nodes = {}
        for idx, row in df.iterrows():
            nodes[row['ID']] = {'id': row['ID'], "code": row['CODE'], "name": row['NAME'], "color": row['COLOR'], 'comment': row['COMMENT'], 'parent': row['PARENT']}

        # Attach child nodes to their parents
        for idx, row in df.iterrows():
            if row['PARENT'] != 0 and row['PARENT'] != -1 :  # If the node has a parent
                parent_node = nodes[row['PARENT']]
                if 'children' not in parent_node:
                    parent_node['children'] = []
                parent_node['children'].append(nodes[row['ID']])

        # Get root nodes
        root_nodes = [node for node_id, node in nodes.items() if
                      df[df['ID'] == node_id]['PARENT'].iloc[0] == -1]
        root_nodes = [{k:v for k,v in node.items() if k != 'parent'} for node in root_nodes]
        layer_nodes.append(
            {'id': layer_idx, 'name': f'Layer {layer_idx} - {layer_names[layer_idx]}', 'children': root_nodes}
        )

    # Convert tree to json
    tree_json = json.dumps(layer_nodes, indent=2)

    # Write json to file
    with open('profiles/tissue_types_v1.json', 'w') as json_file:
        json_file.write(tree_json)
