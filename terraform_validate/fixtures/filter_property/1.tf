resource "aws_one" "some_id_1" {
  filtered_property = "value"
}

resource "aws_one" "some_id_2" {
  not_filtered_property = "value"
}

resource "aws_one" "some_id_3" {
  filtered_property = "value"
}

resource "aws_two" "some_id_1" {
  not_filtered_property = "value"
}

resource "aws_three" "some_id_2" {
  filtered_property = "value"
}