resource "local_file" "foo2" {

  content  = "foo!"

  filename = "${path.module}/foo.bar"

}
 