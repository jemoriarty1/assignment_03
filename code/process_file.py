import streamlit as st
import json
from packaging_parser import (
    parse_packaging,
    calc_total_units,
    get_unit,
)

st.title("Process File of Packages")

package_file = st.file_uploader(
    "Upload package data:", 
    key='package_file'
)

if package_file is not None:
    text = package_file.getvalue().decode("utf-8")
    lines = text.split("\n")

    packages = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        package = parse_packaging(line)
        total = calc_total_units(package)
        unit = get_unit(package)
        packages.append(package)
        st.info(f"{line} ➡️ Total 📦 Size: {total} {unit}")

    json_name = package_file.name.replace(".txt", ".json")
    json_path = f"data/{json_name}"
    with open(json_path, "w") as f:
        json.dump(packages, f)

    st.success(f"{len(packages)} packages written to {json_path}")
