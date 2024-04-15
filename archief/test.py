# def read_highway_names(filename):
#   highway_names = []
#   try:
#     with open(filename, "r") as f:
#       for line in f:
#         highway_names.append(line.rstrip())
#   except FileNotFoundError:
#     print(f"Error: File '{filename}' not found.")
#   return highway_names

# highway_names_list = read_highway_names("data/highway_names.txt")

# if highway_names_list:
#   print("Highway names from file:")
#   for name in highway_names_list:
#     print(name)
# else:
#   print("No highway names found in the file.")
