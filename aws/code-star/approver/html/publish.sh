bucket=cmrsol-xfer
random_bytes=5dbce472088bac28be1b2a2fd6c7166f
s3_key="approver/${random_bytes}/page.html"
aws s3 cp page.html s3://${bucket}/${s3_key}
