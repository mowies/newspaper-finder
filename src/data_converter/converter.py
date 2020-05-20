import json
import re
import time

import spacy

nlp = spacy.load('de')


def main():
    krone_base_path = 'data/krone'
    standard_base_path = 'data/derstandard'
    presse_base_path = 'data/diepresse'
    file_ending_destination = '_preprocessed.txt'
    file_ending_source = '.json'

    labels = [
        '__label__krone',
        '__label__derstandard',
        '__label__diepresse'
    ]

    configs = [
        (krone_base_path + file_ending_source, krone_base_path + file_ending_destination, labels[0]),
        (standard_base_path + file_ending_source, standard_base_path + file_ending_destination, labels[1]),
        (presse_base_path + file_ending_source, presse_base_path + file_ending_destination, labels[2])
    ]

    for infile, outfile, label in configs:
        print("preprocess: " + infile)
        start_time = time.time()
        with open(infile, 'rb') as data_file:
            raw_data = data_file.read().decode('utf8', 'ignore')
            input_data = json.loads(raw_data)

            with open(outfile, 'w', encoding='utf8') as output_file:
                for article in input_data:
                    output_file.write(label + ' ')
                    headline = do_preprocessing(article['headline'])
                    output_file.write(headline + ' ')

                    for line in article['content']:
                        output_file.write(do_preprocessing(line) + ' ')
                    output_file.write('\n')
        end_time = time.time()
        print('needed %0.3f seconds' % (end_time - start_time))


def do_preprocessing(line):
    line = remove_unwanted_symbols(line)
    line = lemmatize(line)
    line = replace_multiple_whitespaces(line)
    return line


def remove_unwanted_symbols(line: str):
    ret = line

    # To lower case
    ret = ret.lower()

    # Remove unwanted symbols and unicode whitespaces
    ret = re.sub(r'[-–/\u00a0\u1680\u180e\u2000-\u200b\u202f\u205f\u3000\ufeff]', ' ', ret)

    # Remove everything in brackets
    ret = re.sub(r'[(\[{].*[)}\]]', '', ret)

    ret = re.sub(r'[^a-zöäüßáćšžíōøčàâçéèêëîïóòôûúùÿðğñæœ ]+', '', ret, flags=re.IGNORECASE)

    return ret


def lemmatize(line):
    doc = nlp(line)

    newline = []
    for token in doc:
        if not token.is_stop:
            newline.append(token.lemma_)
    return ' '.join(newline)


def replace_multiple_whitespaces(line):
    line = re.sub('\s+', ' ', line).strip()
    return line


if __name__ == '__main__':
    main()
