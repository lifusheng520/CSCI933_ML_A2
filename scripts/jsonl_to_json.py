import json
import os


def convert_to_individual_json(file_list):
    for input_file in file_list:
        # check whether file exists
        if not os.path.exists(input_file):
            print(f"File cannot be found: {input_file}")
            continue

        all_records = []

        # read JSONL
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    all_records.append(json.loads(line))

        # construct file name
        output_file = input_file.replace('.jsonl', '.json')

        # write JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_records, f, indent=2, ensure_ascii=False)

        print(f"success：{input_file} -> {output_file} (records length {len(all_records)})")


# files need to be transferred
files = [
    '../data/processed/hamlet_hybrid_chunks.jsonl',
    '../data/processed/macbeth_hybrid_chunks.jsonl',
    '../data/processed/romeo_and_juliet_hybrid_chunks.jsonl'
]

convert_to_individual_json(files)