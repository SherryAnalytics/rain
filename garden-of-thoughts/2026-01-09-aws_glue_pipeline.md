# Bread-and-Butter AWS Engineering  
## Typical AWS Glue Data Pipeline

A common modern AWS data engineering workflow looks like this:

```text
🏛️ Oracle/MS SQL/Teradata Database Extract
          ↓
📄 Raw CSV lands in Amazon S3
          ↓
⚙️ AWS Glue (PySpark) Cleanse / Transform
          ↓
🪶 Write Partitioned Parquet Files
          ↓
📚 AWS Glue Catalog Update
          ↓
🔎 Amazon Athena / 🟥 Amazon Redshift Query
```

---

## 📦 Amazon S3

**S3** stands for **Simple Storage Service**.

A giant object warehouse, where files of all kinds are stored:

- CSV files
- Parquet datasets
- Images
- Logs
- Backups
- Machine learning artifacts

Example object:

```text
s3://voltedge-data/curated/member/2026/01/09/part-0001.parquet
```

Breaking it apart:

| Component | Meaning |
|---|---|
| `s3://` | S3 protocol |
| `voltedge-data` | Bucket name 🪣 |
| `curated/member/2026/01/09/` | Path-like prefix 📁 |
| `part-0001.parquet` | Actual object name 📄 |

---

## 🎭 The Truth About “Folders” in S3

In S3, **folders are mostly an illusion**.

There are no real nested directories like:

```text
/curated/member/2026/01/09/
```

Under the hood, S3 stores everything in a **flat namespace of keys**.

For example:

```text
curated/member/2026/01/09/part-0001.parquet
```

is simply **one long string key**, not a file inside real folders.

AWS Console makes it *look* like folders exist because humans like hierarchy:

```text
📁 curated
   └── 📁 member
       └── 📁 2026
           └── 📁 01
               └── 📁 09
                   └── 📄 part-0001.parquet
```

And we engineers happily work with that illusion every day.

---

## ⚙️ The Pipeline Separates Concerns Cleanly

- **Oracle** → source system 🏛️  
- **S3** → landing / storage zone 📦  
- **Glue + PySpark** → transformation engine ⚙️  
- **Parquet** → analytics-friendly format 🪶  
- **Glue Catalog** → metadata layer 📚  
- **Athena / Redshift** → query & reporting 🔎  

Result:

**Raw operational data → clean analytical dataset → business insights**

---

## 🧠 The classic cloud data assembly line

> **Extract → Land → Clean → Compress → Catalog → Query**
