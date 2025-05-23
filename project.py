import copy


class File:
    def __init__(self, name: str, content: str = ""):
        self.name = name
        self.content = content

    def write_content(self, new_content: str):
        self.content = new_content

    def append_content(self, new_content: str):
        self.content += '\n' + new_content

    def edit_line(self, line_number: int, new_content: str):
        lines = self.content.split('\n')
        if 0 <= line_number < len(lines):
            lines[line_number] = new_content
            self.content = '\n'.join(lines)

    def delete_line(self, line_number: int):
        lines = self.content.split('\n')
        if 0 <= line_number < len(lines):
            lines.pop(line_number)
            self.content = '\n'.join(lines)

    def read_content(self) -> str:
        return self.content


class Folder:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.contents = {}
        self.parent = parent

    def add_item(self, item):
        self.contents[item.name] = item

    def remove_item(self, name: str):
        if name in self.contents:
            del self.contents[name]

    def get_item(self, name: str):
        return self.contents.get(name)

    def list_items(self):
        return list(self.contents.keys())


class FileSystem:
    def __init__(self):
        self.root = Folder("/")
        self.current_folder = self.root

    def get_path_item(self, path: str):
        if path == "/":
            return self.root
        parts = path.strip("/").split("/")
        current = self.root
        for part in parts:
            current = current.get_item(part)
            if not isinstance(current, Folder):
                return None
        return current

    def create_folder(self, args):
        if len(args) == 1:
            folder_name = args[0]
            target_folder = self.current_folder
        elif len(args) == 2:
            path, folder_name = args
            target_folder = self.get_path_item(path)
            if target_folder is None or not isinstance(target_folder, Folder):
                print("Invalid path")
                return
        else:
            print("Usage: mkdir [<path>] <folder_name>")
            return

        if folder_name not in target_folder.contents:
            new_folder = Folder(folder_name, target_folder)
            target_folder.add_item(new_folder)
            print(f"Folder '{folder_name}' created")
        else:
            print("Folder already exists")

    def create_file(self, args):
        if len(args) == 1:
            file_name = args[0]
            target_folder = self.current_folder
        elif len(args) == 2:
            path, file_name = args
            target_folder = self.get_path_item(path)
            if target_folder is None or not isinstance(target_folder, Folder):
                print("Invalid path")
                return
        else:
            print("Usage: touch [<path>] <file_name>.txt")
            return

        if file_name not in target_folder.contents:
            new_file = File(file_name)
            target_folder.add_item(new_file)
            print(f"File '{file_name}' created")
        else:
            print("File already exists")

    def delete_item(self, path: str):
        parts = path.strip("/").split("/")
        folder = self.root
        for part in parts[:-1]:
            folder = folder.get_item(part)
            if not isinstance(folder, Folder):
                print("Invalid path")
                return
        folder.remove_item(parts[-1])

    def write_file(self, name: str):
        file = self.current_folder.get_item(name)
        if isinstance(file, File):
            print("Enter the lines (/end/ means done)")
            content = []
            while True:
                line = input()
                if line == "/end/":
                    break
                content.append(line)
            file.write_content("\n".join(content))
        else:
            print("File not found")

    def append_file(self, name: str):
        file = self.current_folder.get_item(name)
        if isinstance(file, File):
            print("Enter the lines (/end/ means done)")
            content = []
            while True:
                line = input()
                if line == "/end/":
                    break
                content.append(line)
            file.append_content("\n".join(content))
        else:
            print("File not found")

    def cat_file(self, name: str):
        file = self.current_folder.get_item(name)
        if isinstance(file, File):
            print(file.read_content())
        else:
            print("File not found")

    def change_directory(self, name: str):
        if name == "..":
            if self.current_folder.parent:
                self.current_folder = self.current_folder.parent
            else:
                print("Already at root")
        else:
            target = self.current_folder.get_item(name)
            if isinstance(target, Folder):
                self.current_folder = target
            else:
                print("Path not found")

    def list_directory(self):
        print("\n".join(self.current_folder.list_items()))

    def edit_line(self, path: str, line_number: int, content: str):
        file = self.get_path_item(path)
        if isinstance(file, File):
            file.edit_line(line_number, content)

    def delete_line(self, path: str, line_number: int):
        file = self.get_path_item(path)
        if isinstance(file, File):
            file.delete_line(line_number)

    def rename_item(self, path: str, new_name: str):
        parts = path.strip("/").split("/")
        folder = self.root
        for part in parts[:-1]:
            folder = folder.get_item(part)
            if not isinstance(folder, Folder):
                return
        item = folder.get_item(parts[-1])
        if item:
            item.name = new_name
            folder.contents[new_name] = item
            del folder.contents[parts[-1]]

    def move_item(self, source_path: str, dest_path: str):
        parts = source_path.strip("/").split("/")
        source_folder = self.root
        for part in parts[:-1]:
            source_folder = source_folder.get_item(part)
            if not isinstance(source_folder, Folder):
                print("Invalid source path")
                return
        item = source_folder.get_item(parts[-1])
        dest_folder = self.get_path_item(dest_path)
        if item and isinstance(dest_folder, Folder):
            source_folder.remove_item(item.name)
            dest_folder.add_item(item)
        else:
            print("Move failed: Invalid path(s)")

    def copy_item(self, source_path: str, dest_path: str):
        item = self.get_path_item(source_path)
        dest_folder = self.get_path_item(dest_path)
        if item and isinstance(dest_folder, Folder):
            copied_item = copy.deepcopy(item)
            dest_folder.add_item(copied_item)


fs = FileSystem()

while True:
    command = input("$ ").strip()
    if command == "exit":
        break
    parts = command.split()
    cmd = parts[0]

    if cmd == "mkdir":
        fs.create_folder(parts[1:])
    elif cmd == "touch":
        fs.create_file(parts[1:])
    elif cmd == "rm" and len(parts) == 2:
        fs.delete_item(parts[1])
    elif cmd == "cd" and len(parts) == 2:
        fs.change_directory(parts[1])
    elif cmd == "ls":
        fs.list_directory()
    elif cmd == "editline" and len(parts) == 4:
        fs.edit_line(parts[1], int(parts[2]), parts[3])
    elif cmd == "deline" and len(parts) == 3:
        fs.delete_line(parts[1], int(parts[2]))
    elif cmd == "rename" and len(parts) == 3:
        fs.rename_item(parts[1], parts[2])
    elif cmd == "mv" and len(parts) == 3:
        fs.move_item(parts[1], parts[2])
    elif cmd == "cp" and len(parts) == 3:
        fs.copy_item(parts[1], parts[2])
    elif cmd == "nwfiletxt" and len(parts) == 2:
        fs.write_file(parts[1])
    elif cmd == "appendtxt" and len(parts) == 2:
        fs.append_file(parts[1])
    elif cmd == "cat" and len(parts) == 2:
        fs.cat_file(parts[1])
    else:
        print("Unknown command")
