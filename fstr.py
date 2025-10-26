def write_file(path, content):
    try:
        with open(path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

if __name__ == "__main__":
    pass