import pathlib

import tokenize

import io



root = pathlib.Path(__file__).resolve().parent

py_files = sorted(root.rglob('*.py'))

for path in py_files:

    text = path.read_text(encoding='utf-8')

    tokens = tokenize.generate_tokens(io.StringIO(text).readline)

    out = []

    prev_end = (1, 0)

    for tok_type, tok_string, start, end, line in tokens:

        if tok_type == tokenize.COMMENT:

            continue

        if start[0] > prev_end[0]:

            out.append('\n' * (start[0] - prev_end[0]))

            prev_end = (start[0], 0)

        if start[1] > prev_end[1]:

            out.append(' ' * (start[1] - prev_end[1]))

        out.append(tok_string)

        prev_end = end

    new_text = ''.join(out)

    if new_text != text:

        path.write_text(new_text, encoding='utf-8')

        print(f'updated {path.relative_to(root)}')

