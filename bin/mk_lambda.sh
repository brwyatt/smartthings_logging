#!/bin/bash

dir="$(dirname "$(dirname "$(readlink -f $0)")")"
build_dir="${dir}/build"
lambda_dir="${dir}/lambda"
modules_dir="${dir}/src"
dependencies_dir="${dir}/deps"
lib_tmp_path="${build_dir}"
lib_tmp_name="python"
lambda_complete_zip="${build_dir}/lambda_function_complete.zip"
lambda_function_zip="${build_dir}/lambda_function_all.zip"
lambda_layer_zip="${build_dir}/lambda_layer_all.zip"

function filter_dirs() {
    cat \
    | grep -ve '.*\.dist-info$' \
    | grep -ve '.*\.egg-info$' \
    | grep -ve '__pycache__$'
}

cd "${dir}"
if [[ "x${VIRTUAL_ENV}" == "x" ]]; then
    if [ -f env/bin/activate ]; then
       . env/bin/activate
    else
        echo 'Cannot activate virtual environment!' >&2
        exit 1
    fi
fi
python3 setup.py test

if [ $? -ne 0 ]; then
    echo 'Tests failed! Aborting!' >&2
    exit 99
fi

# Setup build directory
echo "Setting up build directory..."
mkdir -p "${build_dir}"
rm -rf "${build_dir}"/*
mkdir -p "${build_dir}/functions" "${build_dir}/layers"

# Process modules dir
echo "Adding package modules..."
cd "${modules_dir}"
zip -r "${lambda_complete_zip}" * -i "*.py"
cd "${lib_tmp_path}"
ln -s "${modules_dir}" "${lib_tmp_name}"
zip -r "${lambda_layer_zip}" "${lib_tmp_name}" -i "*.py"
for file in $(ls "${lib_tmp_name}" | filter_dirs); do
    zip -r "${build_dir}/layers/${file}.zip" "${lib_tmp_name}/${file}" -i "*.py"
done
rm -f "${lib_tmp_name}"

# Process Lambda dir
echo "Adding Lambda functions..."
cd "${lambda_dir}"
zip -r "${lambda_complete_zip}" * -i "*.py"
zip -r "${lambda_function_zip}" * -i "*.py"
for file in $(ls); do
    zip -r "${build_dir}/functions/${file:0:-3}.zip" "${file}"
done

# Process dependencies dir
echo "Adding dependency modules..."
cd "${dir}"
mkdir -p "${dependencies_dir}"
rm -rf "${dependencies_dir}"/*
grep -ive '^boto3[=<>]' requirements.txt | pip3 install -r /dev/stdin --target "${dependencies_dir}"
cd "${dependencies_dir}"
zip -r "${lambda_complete_zip}" * -i "*.py"
cd "${lib_tmp_path}"
ln -s "${dependencies_dir}" "${lib_tmp_name}"
zip -r "${lambda_layer_zip}" * -i "*.py"
for file in $(ls "${lib_tmp_name}" | filter_dirs); do
    if [[ "${file}" == *".py" ]]; then
        filename="${file:0:-3}"
    else
        filename="${file}"
    fi
    zip -r "${build_dir}/layers/${filename}.zip" ""${lib_tmp_name}"/${file}" -i "*.py"
done
rm -f "${lib_tmp_name}"

# vim: ts=4 sts=4 sw=4 expandtab
