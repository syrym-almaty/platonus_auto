import json
import os
import logging
from tqdm import tqdm
import validators
import argparse

def extract_profile_links(input_filepath, output_filepath):
    """
    Extracts all valid 'profile_link' values from the input JSON file and saves them to the output JSON file.

    Parameters:
    - input_filepath (str): Path to the input JSON file containing student data.
    - output_filepath (str): Path where the output JSON file with links will be saved.
    """
    try:
        # Configure logging
        logging.basicConfig(
            filename='extract_links.log',
            filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

        # Check if input file exists
        if not os.path.exists(input_filepath):
            logging.error(f"The input file '{input_filepath}' does not exist.")
            raise FileNotFoundError(f"The input file '{input_filepath}' does not exist.")

        # Load data from the input JSON file
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            logging.info(f"Loaded {len(data)} records from '{input_filepath}'.")

        # Extract 'profile_link' from each object with progress bar
        links = []
        missing_links = 0
        invalid_links = 0
        for record in tqdm(data, desc="Extracting profile links"):
            link = record.get('profile_link')
            if link and validators.url(link):
                links.append(link)
            else:
                missing_links += 1
                if link:
                    invalid_links += 1
                    logging.warning(f"Invalid URL format: {link} (Record ID: {record.get('id')})")
                else:
                    logging.warning(f"Missing 'profile_link' (Record ID: {record.get('id')})")

        logging.info(f"Extracted {len(links)} valid links.")
        if missing_links > 0:
            logging.info(f"Total records missing 'profile_link': {missing_links - invalid_links}")
            logging.info(f"Total records with invalid 'profile_link': {invalid_links}")

        # Prepare the output dictionary
        output_data = {"links": links}

        # Save the links to the output JSON file
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            json.dump(output_data, outfile, ensure_ascii=False, indent=4)
            logging.info(f"Successfully saved links to '{output_filepath}'.")

        print(f"Extraction completed. {len(links)} links saved to '{output_filepath}'.")
        if missing_links > 0:
            print(f"Some records were missing or had invalid 'profile_link'. Check 'extract_links.log' for details.")

    except json.JSONDecodeError:
        logging.error(f"The file '{input_filepath}' is not a valid JSON file.")
        print(f"Error: The file '{input_filepath}' is not a valid JSON file.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Extract profile links from student data JSON.")
    parser.add_argument('--input', type=str, required=True, help='Path to the input students_data.json file.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output links.json file.')

    args = parser.parse_args()

    extract_profile_links(args.input, args.output)

if __name__ == "__main__":
    main()
