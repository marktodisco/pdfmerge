import argparse
from pathlib import Path
from typing import List, Sequence, Union


def parse_arguments(
    args: Union[List[str], argparse.Namespace]
) -> argparse.Namespace:
    if isinstance(args, argparse.Namespace):
        return args
    parser = argparse.ArgumentParser(
        prog='pdfmerge', description="Merge pdf files."
    )
    parser.add_argument(
        '-f', '--files', nargs='*', help='File names.', default=None
    )
    parser.add_argument(
        '-o', '--output-name', help='Output file name.', default=None
    )
    parser.add_argument(
        '-d', '--input-dir', help='Input directory.', default=None
    )
    return parser.parse_args(args)


def get_files(args: argparse.Namespace) -> Sequence[str]:
    if args.files is not None:
        return args.files
    elif args.input_dir is not None:
        return [str(path) for path in Path(args.input_dir).glob('*.pdf')]
    else:
        raise ValueError(f'Invalid files: {args.files}')


def validate_paths_and_handle_error(paths: Sequence[str]) -> Sequence[str]:
    invalid_paths = list(filter(lambda path: not Path(path).exists(), paths))
    if len(invalid_paths) > 0:
        raise FileNotFoundError(invalid_paths)
    paths = [Path(path).resolve().as_posix() for path in paths]
    return paths


def validate_files_and_handle_error(files: Sequence[str]) -> Sequence[str]:
    for file in files:
        if not Path(file).suffix == '.pdf':
            raise ValueError(f'{file} is not a PDF')
    return [(Path('.').resolve() / file).as_posix() for file in files]


def validate_output_name_and_handle_error(output_name: str) -> str:
    output_name_ = Path(output_name)
    if output_name_.suffix != '.pdf':
        raise ValueError(f'{output_name_} is not a PDF')
    return (Path('.').resolve() / output_name_).as_posix()
