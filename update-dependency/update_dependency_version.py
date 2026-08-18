import sys
import tomlkit
from tomlkit import TOMLDocument
from tomlkit.items import InlineTable, Table


def try_update(deps_table, location_label: str, package_name: str, new_version: str) -> bool:
    if deps_table is None:
        return False

    if package_name in deps_table:
        key = package_name
    else:
        # Try case-insensitive search
        key = next((k for k in deps_table if k.lower() == package_name.lower()), None)
        if key is None:
            return False

    current = deps_table[key]
    if isinstance(current, (InlineTable, Table, dict)):
        current["version"] = new_version
    else:
        deps_table[key] = new_version

    print(f"Updated {key} -> {new_version} in {location_label}")
    return True


def find_and_update(doc: TOMLDocument, package_name: str, new_version: str) -> bool:
    """Search main and dev-group dependency tables for the package and update its version in place."""
    tool_table = doc.get("tool")
    poetry = tool_table.get("poetry", {}) if tool_table is not None else {}

    updated = False

    # [tool.poetry.dependencies]
    if try_update(poetry.get("dependencies"), "tool.poetry.dependencies", package_name, new_version):
        updated = True

    # [tool.poetry.group.dev.dependencies]
    group = poetry.get("group", {})
    dev_group = group.get("dev", {}) if group else {}
    if try_update(dev_group.get("dependencies"), "tool.poetry.group.dev.dependencies", package_name, new_version):
        updated = True

    return updated


def main():
    if len(sys.argv) != 4:
        print("Usage: update_dep_version.py <pyproject.toml path> <package_name> <new_version>")
        sys.exit(1)

    path, package_name, new_version = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(path, "r") as f:
        doc = tomlkit.parse(f.read())

    if not find_and_update(doc, package_name, new_version):
        print(f"::error::{package_name} not found in tool.poetry.dependencies or tool.poetry.group.dev.dependencies in {path}")
        sys.exit(1)

    with open(path, "w") as f:
        f.write(tomlkit.dumps(doc))


if __name__ == "__main__":
    main()
