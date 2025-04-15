variable "files" {
     default = [
       "file0.txt",  # index 0
       null,         # index 1 - delete record
       "file2txt",   # index 2
       "file3.txt",  # index 3
       "file4.txt"   # index 4
     ]
   }
 
 
 
resource "local_file" "foo1" {
  for_each = {
    for idx, filename in var.files : idx => filename
    if filename != null
  }
 
  content  = "# Some content for file ${each.key}"
  filename = each.value
}
 
 