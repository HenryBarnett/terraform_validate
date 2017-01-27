data "template_file" "init" {
    template = "${file("${path.module}/init.tpl")}"

    vars {
        consul_address = "${aws_instance.consul.private_ip}"
    }
}

data "archive_file" "init" {
    type        = "zip"
    source_file = "${path.module}/init.tpl"
    output_path = "${path.module}/files/init.zip"
}