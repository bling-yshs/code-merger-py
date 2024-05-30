import os

import pyperclip
import tiktoken


def is_text_file(file_path):
    try:
        with open(file_path, encoding='utf-8') as f:
            f.read()
        return True
    except (UnicodeDecodeError, IOError):
        return False


def process_folder(folder_path, output_file):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_text_file(file_path):
                relative_path = os.path.relpath(file_path, folder_path)
                output_file.write(f"> {relative_path}\n")
                with open(file_path, encoding='utf-8') as f:
                    content = f.read()
                    output_file.write("```\n")
                    output_file.write(content)
                    output_file.write("\n```\n\n")


def count_tokens(file_path):
    with open(file_path, encoding='utf-8') as f:
        content = f.read()
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(content)
    return len(tokens)


def main():
    folder_path = input("请输入文件夹路径：")
    output_path = 'output.md'

    with open(output_path, 'w', encoding='utf-8') as output_file:
        process_folder(folder_path, output_file)

    token_count = count_tokens(output_path)
    print(f"合并完成，结果保存在 {output_path} 中。")
    print(f"output.md 的 token 数为：{token_count}")
    # 读取文件内容并复制到剪贴板
    with open(output_path, encoding='utf-8') as f:
        content = f.read()
    pyperclip.copy(content)
    print("已将输出内容复制到剪贴板")


if __name__ == '__main__':
    main()
