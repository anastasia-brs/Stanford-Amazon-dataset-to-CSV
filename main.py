import getopt
import mmap
import re
import sys

INPUT_FILE_PATAMETER_NAME = 'input_txt'
OUTPUT_FILE_PARAMETER_NAME = 'output_csv'

DATASET_COLUMNS = 'productId,' \
                  'title,' \
                  'price,' \
                  'userId,' \
                  'profileName,' \
                  'helpfulness,' \
                  'score,' \
                  'time,' \
                  'summary,' \
                  'text\n'.encode('utf-8')

REGEXP = 'product\/productId: (.*)\s*' \
         'product\/title: (.*)\s*' \
         'product\/price: (.*)\s*' \
         'review\/userId: (.*)\s*' \
         'review\/profileName: (.*)\s*' \
         'review\/helpfulness: (.*)\s*' \
         'review\/score: (.*)\s*' \
         'review\/time: (.*)\s*' \
         'review\/summary: (.*)\s*' \
         'review\/text: (.*)\s*'.encode('utf-8')

# Example:
# python main.py -i books.txt -o books.csv
commandLineFormat = '-i --%s \n\t-  the input TXT dataset file name \
                    -o --%s \n\t-  the output CSV file name' \
                    % (INPUT_FILE_PATAMETER_NAME, OUTPUT_FILE_PARAMETER_NAME)


def init_from_args(argv):
    input_txt = None
    output_csv = None

    try:
        opts, args = getopt.getopt(argv, "hi:o:",
                                   [INPUT_FILE_PATAMETER_NAME + '=',
                                    OUTPUT_FILE_PARAMETER_NAME + '='])
    except getopt.GetoptError:
        print(commandLineFormat)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(commandLineFormat)
            sys.exit()
        elif opt in ("-i", "--" + INPUT_FILE_PATAMETER_NAME):
            input_txt = arg
        elif opt in ("-o", "--" + INPUT_FILE_PATAMETER_NAME):
            output_csv = arg

    print('Input TXT file:\n\t%s' % input_txt)
    print('Output CSV file:\n\t%s' % output_csv)
    return input_txt, output_csv


def read_file(file_path):
    print('Read input \'%s\' file.' % file_path)

    opened_file = open(file_path, 'r', encoding='utf-8')
    return mmap.mmap(opened_file.fileno(), 0, access=mmap.ACCESS_READ)


def parse(data):
    print('Find items.')
    return re.findall(REGEXP, data)


def write_column_names(output_file):
    print('Write column names.')
    output_file.write(DATASET_COLUMNS)


def export_to_csv(parsed_data, file_path):
    print('Write output \'%s\' file.' % file_path)
    output_file = open(file_path, 'wb')

    print('Export items data.')
    write_column_names(output_file)
    for item in parsed_data:
        item_without_quotes = list(map(lambda x: b'"' + x.replace(b'"', b'\\"') + b'"', item))
        output_file.write(b','.join(item_without_quotes))
        output_file.write(b'\n')


def main(argv):
    input_file, output_file = init_from_args(argv)

    input_data = read_file(input_file)
    parsed_data = parse(input_data)

    export_to_csv(parsed_data, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
