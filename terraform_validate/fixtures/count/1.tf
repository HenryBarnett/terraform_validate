resource "aws_instance" "with_name" {
  count = "3"
  private_ip = "${lookup(var.instance_ips, count.index)}"
  name = "overwrite"
}

resource "aws_instance" "with_name_unique" {
  count = "3"
  private_ip = "${lookup(var.instance_ips, count.index)}"
  name = "overwrite_${count.index}"
}

resource "aws_instance" "with_no_name" {
  count = "3"
  private_ip = "${lookup(var.instance_ips, count.index)}"
}