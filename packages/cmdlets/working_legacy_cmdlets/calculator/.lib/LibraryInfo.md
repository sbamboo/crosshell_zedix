## Libary files and file-structures.

### What are they?

*.lib* files are files that contain addtions for my code projects.

### How do they work?

They use a polygott code format and may include either only executable code or a polygott structure of code and a zip section.

Which one is used must be defined in a head line (or libhead line)

### Formats:

There are currently 4 formats accessible and a fifth one comming in the future.

- **Format-0**: This format contains only code (**CodeOnly**)
- **Format-1**: This format is a polygott of Code and Archive, were the archive section comes first in the file. (**Obs!** This format only allows 1 code section and 1 archive section) (**ZipFirst**)
- **Format-2**: This format is a polygott of Code and Archive, were the archive section comes last in the file. (**Obs!** This format only allows 1 code section and 1 archive section) (**ZipLast**)
- **Format-3**: This format contains only an archive section and no code (**ZipOnly**)

NonImplomented:

- **Format-4**: (*ExtendedLibraryFormat*) or ELF is a format still in development, the format will have new features and allow for more variants of lib files.

### LibHead:   (Not always a header)

The libhead contains information regarding the polygot format/structure of the file.

- Format: Defines format of the file. **0: CodeOnly, 1: ZipFirst, 2: ZipLast, 3: ZipOnly, 4: ELF**   (Zip can be any universal archive structure but must be defined it in the **Alng**)
- Lang: *Defines language of the code section.***-FileExtensionOfLanguage**
- Alng: *Defines language of the archive section.***-FileExtensionOfArchive**
- Exec: *Defines what executable to be used in sertain situations* **-HostCommandForTheExecutable**

Example LibHead:

```
§Format:1,Lang:.ps1,Alng:.zip,Exec:Pwsh§
```

Some times the `§` characters might have a `Â` character before them, this is because of file formating.

### **Reading the files:**

Lib files including a zip section can be extraced either by renaming the file to *.zip* or by extracting it in code or by a program like *7zip*.

The code section depends on what language you are using and how it handles running over the zip sections.

- For powershell you need some code to only load code after or before the libhead (Depending on format)

**Code for that:**

```
#LibaryLoader by Simon Kalmi Claesson
#Ver: 1.0
#

$file = "examplelib.lib"
$tmp = Get-Content "$file"
$useformat = "§Format:1"
$tmp1 = ""
$sof_found = "0"
foreach ($l in $tmp) {
if ($l -like "*$useformat*") {$sof_found = "1"}
if ($sof_found -eq "1") {
if ($l -notlike "*$useformat*") {
$tmp1 += "$l`n"
}
}
}
if ($sof_found -ne "0") {$sof_found = "0"}

Invoke-Expression "$tmp1"
```

***(In a .ps1 file)***

### SpecSheet:

##### **InCode:**

In the code the library metadata must be defined. The data should be defined as *open* variables in the codes language. *(Open means that the variable is accessable by the reader code)*

The variables must follow a sertain name scheme:

`<libraryName>`_Version

`<libraryName>`_Author

`<libraryName>`_Description

`<libraryName>`_IsCombi

*LibraryName* **is replaced by the name of the library**

*IsCombi is boolean and defines if the library is a polygot.*

##### **InArchive:**

InArchive formats allow for multiple files (Of code and resources) to be bundled in the archive section.

Just like in the *InCode* section, libmeta data must be defined. However in a archive format the metadata is defined in a *.libmeta* file. (The libmeta file is NOT optional)

The file uses Json formating and needs to have specific names.

- Version
- Author
- Description
- IsCombi

An example of a libbeta file is:

```
{"lib":{
  "Version":     {"value":"3.0"},
  "Author":      {"value":"Simon Kalmi Claesson"},
  "Description": {"value":""},
  "IsCombi":     {"value":"True"}
}}
```

Furthermore then the libmeta file, the archive must contain one main code file named after the libraryname.

*(Example: `<libraryName>.ps1`, If your library is named "example" the main code file must be named "example", the fileextension is dependent of the code language)*

**OBS!** In format 1-3 the libraryname must be the same as the *.lib* file.  (It format-4 is can be defined but if not this will also apply)

---

Hope this information is of any help 😊

(This information is shared to help with understanding the idea behind the format, and understanding the .lib files, for information on how to create library files go to: [Creating_lib_files](https://sites.google.com/view/scofficial/docs/library/creating_lib_files/))
