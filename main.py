import re
import sys


def verify_log(file_path):
    unit_name   = ''
    class_name  = ''
    method_name = ''
    log_name    = ''
    line_errors = []

    with open(file_path, 'r', encoding='windows-1252') as f:
        lines = f.readlines()

    for i, line in enumerate(lines, start=1):
        try:
            # armazena nome da unit e da classe (nao mudam)
            find_unit = re.search(rf'unit.*;', line)
            if find_unit:
                unit_name = line.split(' ')[1]
                unit_name = re.split(rf';', unit_name)[0]
                class_name = 'T' + unit_name[:-1]

            # armazena nome do metodo (muda a cada metodo)
            find_method = re.search(rf'(procedure|function|constructor|destructor).*{class_name}\.', line)
            if find_method:
                method_name = line.split('.')[1]
                method_name = re.split(rf';|\(|:', method_name)[0]

            # armazena log de LogError, LogException ou m_EventWriter
            find_log = re.search(rf'(LogError\(|LogException\(|EventWriter.WriteMsg\(\')', line)
            if find_log:
                log_name = line.split('\'')[1]
                log_name = re.split(rf':| ', log_name, 1)[0]

                expected_log = f'{class_name}.{method_name}'
                if log_name.strip() != expected_log.strip():
                    line_errors.append((i, log_name, expected_log))
        except:
            pass

    return line_errors


def print_errors(errors):
    with open('log_errors.txt', 'w') as file:
        if errors:
            for line, log_name, expected_log in errors:
                file.write(f'LINE: {line}; EXPECTED_LOG: {expected_log}; FOUNDED_LOG: {log_name};\n\n')
        else:
            file.write('everything is fine.\n')


def main():
    if len(sys.argv) > 1:
        file_path = f'{sys.argv[1]}'
        errors = verify_log(file_path)
        print_errors(errors)
        print('done! check out the log_errors.txt file.')
    else:
        print('inform the path file as argument.')


if __name__ == '__main__':
    main()
