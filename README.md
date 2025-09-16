# grouping-files-by-extension


````markdown
# File Organizer

A simple script to organize files in a directory by their extension. It groups files into separate folders based on their file types (e.g., .jpg, .txt, .pdf), making it easier to manage and organize your files. You can also undo the last movement.

## Features

- **Organizes files** by their extensions into corresponding folders.
- **Dry-run mode** for testing (no changes made).
- **Undo** functionality to revert the last file movement.
- **Logs** all movements in a `moves.json` file for tracking.

## How to Use

### 1. Organize Files

To run the organizer in **dry-run** mode (no changes are made, only logs the operations):

```bash
python organize.py /path/to/directory
````

To **actually move** the files:

```bash
python organize.py /path/to/directory --run
```

### 2. Undo the Last Move

To undo the last file movement (reverts the file back to its original location):

```bash
python organize.py /path/to/directory --undo
```

### Example

First, create some test files in a folder (you can skip this if you already have files to organize):

```python
ext = '.jpg .txt .xlsx .pdf .tar.gz'.split(' ')
for i in ext:
    with open(f'teste/teste_files/teste{i}', 'w+') as arch:
        arch.write('')
```

Now, run the organizer to move the files into folders based on their extensions:

```bash
python organize.py /path/to/teste/teste_files
```

This will move the `.jpg` files into a "jpg" folder, `.txt` files into a "txt" folder, etc.

### Logging and Undoing

All file movements are logged in a `moves.json` file. You can use the `--undo` option to revert the last operation, moving the files back to their original locations.

## Requirements

* Python 3.x
* Required Python libraries: `shutil`, `argparse`, `re`, `json`, `time`, `logging`

## License

This project is open-source and available under the [MIT License](LICENSE).


