export function isEmpty(list) {
    return !list || list.length === 0;
}

export function lowerCaseFileExtension(filePath) {
    const extension = filePath.substring(filePath.lastIndexOf('.') + 1);
    const lowerCaseExtension = extension.toLowerCase();
    return filePath.replace(extension, lowerCaseExtension);
}