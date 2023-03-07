# Tabledraw: Library made by Simon Kalmi Claesson
# Includes a drawTable function that takes a dictionary width colums where each element is a row. And renders a table from it.
# Example: Where bob has 10 and marie has 20
# data = {
#   "Players": {"bob","marie"},
#   "Stats":   {"10","20"}
# }
# 

# Function to take dictionary and render table
def drawTable(data=dict()):
    # extract the headers from the dictionary keys
    headers = list(data.keys())

    # [calculate the width of each column]
    widths = []
    # iterate over each header to calculate the maximum width of that column
    for header in headers:
        # Assume lenght is header length plus 2 padding spaces
        width = len(header) + 2
        # iterate over each value in the column to find the maximum width of that value
        for value in data[header]:
            # Length: len() + 2 spaces
            value_width = len(str(value)) + 2
            # Update column width if found string longer than first assumption
            width = max(width, value_width)
        # add the final column width to the list of widths
        widths.append(width)

    # print the tables top
    print("╭" + "┬".join("─" * width for width in widths) + "╮")

    # print the headers
    if len(headers) > 0:
        header_row = "│"
        for header, width in zip(headers, widths):
            # center the header string in its column and add padding spaces on either side
            header_row += header.center(width) + "│"
        print(header_row)

    # print the divider row
    print("├" + "┼".join("-" * width for width in widths) + "┤")

    # print each value row
    if len(headers) > 0:
        for i in range(len(data[headers[0]])): # Get amount of rows under first column and use this to determin a range
            if data[headers[2]][i] == "won": colval = "\033[33m" # If won, print in yellow
            else: colval = "\033[31m" # Else print in red
            value_row = "│"
            for header, width in zip(headers, widths): # Associate headers with their widths
                # center the value string in its column and add padding spaces on either side
                try:
                    value_row += colval + str(data[header][i]).center(width) + "\033[0m│" # Try/except incase empty row in column
                except: value_row += str(header).center(width) + "│"
            print(value_row)

    # print the bottom of the table
    print("╰" + "┴".join("─" * width for width in widths) + "╯")
