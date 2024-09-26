# Assignment Tasks

1. Verify the project setup using the instructions above.

2. Update the `SW_ASSIGNMENT_PREFIX` environment variable to only print the 
dicom folders (`dicom1`, `dicom2`, `dicom3`).

3. Implement a suffix filter (the file extension) feature:
   - Add a suffix filter to the configuration / environment variables.
   - Filter files based on the suffix.
   - Include the suffix as an explicit field/column in the output (StdoutPrinter and JsonPrinter).
   - Add tests for this feature.
   - Before continuing, ensure the tests and linters pass.

4. Implement DICOM folder filtering:
   - Change the code to only print files inside DICOM folders.
   - A DICOM folder is defined as:
     * One and only one text file (.txt)
     * At least two DICOM files (.dcm)
   - Assume the bucket only contains folders, and these folders only contain files (no nested folders).
   - Tests are not required for this feature.