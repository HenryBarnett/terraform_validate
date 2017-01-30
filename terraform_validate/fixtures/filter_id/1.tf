resource "aws_security_group" "some_id_2" {
  vpc_id = "${aws_vpc.main.id}"
  name = "name_value"
}

resource "aws_security_group" "some_id_3" {
  vpc_id = "${aws_vpc.main.id}"
  name = "name_value"
}

resource "aws_security_group2" "some_id_3" {
  vpc_id = "${aws_vpc.main.id}"
  name = "name_value"
}

resource "aws_isntance" "some_id_1" {
  vpc_id = "${aws_vpc.main.id}"
  name = "name_value"
}

resource "aws_isntance" "some_id_2" {
  vpc_id = "${aws_vpc.main.id}"
  name = "name_value"
}