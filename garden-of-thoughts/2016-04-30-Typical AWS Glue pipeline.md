[Bread-and-butter AWS engineering]
Typical AWS Glue pipeline

Oracle extract
↓
raw CSV lands in S3
↓
Glue PySpark cleanse / transform
↓
write partitioned Parquet
↓
Glue Catalog update
↓
Athena / Redshift query

S3 = Simple Storage Service

Object Key = s3://calstrs-data/curated/member/2026/04/27/part-0001.parquet

in S3, “folders” are mostly an illusion. It’s really a flat key namespace wearing folder clothes, a little theatrical set design 🎭. But engineers happily work with the illusion every day.
