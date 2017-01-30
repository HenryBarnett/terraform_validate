resource "type_one" "some_id_1" {
  vpc_id = "${aws_vpc.main.id}"
  name = "name_value"
}

resource "type_two" "some_id_2" {
  vpc_id = "${aws_vpc.main.id}"
  name = "name_value"
}

resource "type_three" "some_id_2" {
  vpc_id = "${aws_vpc.main.id}"
  name = "name_value"
}

resource "type_four" "some_id_3" {
  vpc_id = "${aws_vpc.main.id}"
  name = "name_value"
}

resource "type_one" "some_id_2" {
  vpc_id = "${aws_vpc.main.id}"
  name = "name_value"
}