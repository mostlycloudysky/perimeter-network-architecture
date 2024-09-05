resource "aws_db_instance" "app_db" {
  identifier             = "app-db"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "13.11"
  instance_class         = "db.t3.micro"
  username               = "dbadmin"             # Reference only and should be secured in terraform workspace env.
  password               = "supersecurepassword" # Reference only and should be secured in terraform workspace env.
  db_subnet_group_name   = aws_db_subnet_group.app_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  multi_az               = true
  publicly_accessible    = false
  storage_type           = "gp2"
  skip_final_snapshot    = true
}

resource "aws_db_subnet_group" "app_db_subnet_group" {
  name       = "app-db-subnet-group"
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]
}
