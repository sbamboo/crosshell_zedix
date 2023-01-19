# Get argv as string
stringInput = (' '.join(argv)).strip(" ")

stringInput = stringInput.strip('"')

# Check if directory exists
if os.path.exists(stringInput):

    # Load cmdlets inside directory
    packagePathables = cs_loadCmdlets(stringInput,allowedFileTypes)
    for pathable in packagePathables:
        cspathables.append(pathable)