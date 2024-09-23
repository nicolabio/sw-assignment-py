
1. Verify project. See README.md for more details.  

2. Next, we want to improve this tool by adding a filter to print files of a 
certain type (suffix). For example, to only print .dcm files.
* Add a suffix filter to the configuration / environment variables.
* Use this filter the suffix of the files. 
* Include in the output (StdoutPrinter and the JsonPrinter) the suffix as an 
explicit field/column. 
* Make sure to add tests for this feature.

3. TODO(ILIAS): Some devopsish task.

Now, we are printing all folders, and only filter on prefix and suffix. However, 
imagine that a dicom folder has a slightly more complex definition.

Let's say that a DICOM folder is defined as: 
* One and only one text file (.txt). 
* At least two dicom files (.dcm). 

You may assume that the bucket only contains folders, and that these folders
only contain files (no nested folders). 

4. Change the code such that only the files inside dicom folders are printed. 
You don't have to write tests for this feature. And you don't need to add an 
environment variable for this feature.
