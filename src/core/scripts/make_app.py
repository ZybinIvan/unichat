import os


def create_structure(folder_name: str):
    """
    Создаёт папку folder_name и внутри неё файлы:
    models.py, providers.py, repositories.py,
    routes.py, schemas.py, services.py, use_cases.py
    """
    # Список файлов для создания
    files = [
        "__init__.py",
        "models.py",
        "providers.py",
        "repositories.py",
        "routes.py",
        "schemas.py",
        "services.py",
        "use_cases.py",
    ]

    # Создаём папку (если уже есть — не падает)
    os.makedirs(folder_name, exist_ok=True)

    # Создаём все файлы внутри папки
    for filename in files:
        file_path = os.path.join(folder_name, filename)
        # Если нужно, можно добавить boilerplate-заголовок
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# Файл {filename}\n\n")

    print(f"Папка '{folder_name}' и файлы внутри успешно созданы.")


if __name__ == "__main__":
    name = input("Введите расположение и название новой папки: ").strip()
    if not name:
        print("Название папки не может быть пустым.")
    else:
        create_structure(name)
