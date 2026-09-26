import streamlit as st
import json
from packaging_parser import (
    parse_packaging,
    calc_total_units,
    get_unit,
)

st.title("Process Package Files")

if "files_processed" not in st.session_state:
    st.session_state.files_processed = 0
if "packages_processed" not in st.session_state:
    st.session_state.packages_processed = 0
if "file_summaries" not in st.session_state:
    st.session_state.file_summaries = []

package_file = st.file_uploader(
    "Upload package data:", 
    key='package_file'
)

process_clicked = st.button(
    "Process", 
    key="process"
)

if process_clicked and package_file is not None:
    text = package_file.getvalue().decode("utf-8")
    lines = text.split("\n")

    packages = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        package = parse_packaging(line)
        packages.append(package)

    json_name = package_file.name.replace(".txt", ".json")
    json_path = f"data/{json_name}"
    with open(json_path, "w") as f:
        json.dump(packages, f)

    st.session_state.files_processed += 1
    st.session_state.packages_processed += len(packages)
    st.session_state.file_summaries.append(
        f"{package_file.name} ➡️ {len(packages)} packages written to {json_path}"
    )

col1, col2 = st.columns(2)
col1.metric("Files processed", st.session_state.files_processed)
col2.metric("Packages processed", st.session_state.packages_processed)


for summary in st.session_state.file_summaries:
    st.info(summary)