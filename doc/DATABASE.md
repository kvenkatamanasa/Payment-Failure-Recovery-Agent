# Database Documentation

## 1. Overview

The AI Payment Failure Recovery Agent uses Django ORM for database operations.

The production environment uses:

```text
PostgreSQL
     |
     v
Supabase
```

The application contains two primary project models:

* Payment
* RecoveryAudit

Django's built-in User model is also used.

---

# 2. Entity Relationship

```text
+----------------+
|      User      |
+----------------+
| id             |
| username       |
| email          |
| password       |
+-------+--------+
        |
        | creates
        v
+----------------+
|    Payment     |
+----------------+
| id             |
| transaction_id |
| amount         |
| status         |
| failure_type   |
| created_at     |
+-------+--------+
        |
        | generates
        v
+----------------+
| RecoveryAudit  |
+----------------+
| id             |
| payment        |
| diagnosis      |
| confidence     |
| recommendation |
| decision       |
| created_at     |
+----------------+
```

---

# 3. User Model

Django provides the authentication User model.

It is used for:

* Registration
* Login
* Logout
* Authentication
* Authorization
* Administrator accounts

Typical information includes:

```text
id
username
email
password
first_name
last_name
is_staff
is_superuser
```

Passwords are managed by Django's authentication system.

---

# 4. Payment Model

The Payment model stores transaction information.

Typical fields include:

| Field            | Purpose                       |
| ---------------- | ----------------------------- |
| `id`             | Primary key                   |
| `transaction_id` | Unique transaction identifier |
| `amount`         | Payment amount                |
| `status`         | Payment status                |
| `failure_type`   | Failure scenario              |
| `created_at`     | Transaction timestamp         |

Example:

```text
Transaction ID : PAY-10245
Amount         : INR 1500
Status         : Failed
Failure Type   : Network Error
```

---

# 5. Payment Status

Possible payment states can include:

```text
Pending
Successful
Failed
Recovered
```

The exact available values depend on the implementation in `payments/models.py`.

---

# 6. Failure Type

The failure type identifies why a payment failed.

Supported scenarios include:

```text
Payment Timeout
Network Error
Insufficient Balance
Payment Declined
Bank Error
UPI Failure
Gateway Server Error
Invalid Payment Details
Authentication Failure
```

---

# 7. RecoveryAudit Model

The RecoveryAudit model stores information about recovery decisions.

Typical information includes:

| Field                | Purpose              |
| -------------------- | -------------------- |
| `payment`            | Related payment      |
| `diagnosis`          | AI diagnosis         |
| `confidence`         | Diagnosis confidence |
| `recommended_action` | Suggested recovery   |
| `decision`           | Recovery decision    |
| `created_at`         | Audit timestamp      |

---

# 8. Relationship Between Payment and Audit

One payment can have recovery-related audit information.

Conceptually:

```text
Payment
   |
   +---- RecoveryAudit
   |
   +---- RecoveryAudit
```

The exact relationship depends on the model definition.

---

# 9. Database Flow

```text
User
 |
 v
Payment Created
 |
 v
Payment Failure Recorded
 |
 v
AI Diagnosis
 |
 v
Recovery Decision
 |
 v
RecoveryAudit Created
 |
 v
Database
```

---

# 10. Django ORM

Django ORM is used instead of writing raw SQL for most database operations.

Example:

```python
Payment.objects.create(
    transaction_id="PAY-10245",
    amount=1500,
    status="Failed",
    failure_type="Network Error"
)
```

Query example:

```python
failed_payments = Payment.objects.filter(
    status="Failed"
)
```

---

# 11. PostgreSQL

The production system uses PostgreSQL because it provides:

* Reliability
* Scalability
* Transaction support
* Strong data integrity
* Production database capabilities

Supabase provides the hosted PostgreSQL database.

---

# 12. Database Migrations

Django migrations manage database schema changes.

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

View migration status:

```bash
python manage.py showmigrations
```

---

# 13. Database Security

Database credentials must never be committed to GitHub.

Use environment variables:

```env
DATABASE_URL=your-database-url
```

The actual production database password must remain private.

---

# 14. Production Database Architecture

```text
Vercel
  |
  | DATABASE_URL
  v
Supabase PostgreSQL
  |
  +---- auth data
  |
  +---- payment data
  |
  +---- recovery audit data
```

---

# 15. Backup and Recovery

For production deployments, database backups should be configured through the database provider.

The application itself should not store production database credentials inside source code.

---

# 16. Summary

The database layer provides persistent storage for:

* Users
* Payments
* Failure scenarios
* AI diagnoses
* Recovery decisions
* Audit records

The combination of Django ORM and PostgreSQL provides a structured and maintainable data layer.

```
```
