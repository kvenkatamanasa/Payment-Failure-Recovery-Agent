# System Architecture

## 1. Overview

The AI Payment Failure Recovery Agent follows a layered web application architecture.

```text
                    USER
                     |
                     v
             +---------------+
             |   Frontend    |
             | HTML / CSS    |
             +---------------+
                     |
                     v
             +---------------+
             |    Django     |
             |   Web Layer   |
             +---------------+
                     |
          +----------+----------+
          |                     |
          v                     v
   +-------------+       +-------------+
   | Payment     |       | AI Diagnosis|
   | Processing  |       | Engine      |
   +-------------+       +-------------+
          |                     |
          +----------+----------+
                     |
                     v
             +---------------+
             |    Safety     |
             |  Guardrails   |
             +---------------+
                     |
             +-------+-------+
             |               |
             v               v
       Recovery Allowed   Recovery Blocked
             |               |
             +-------+-------+
                     |
                     v
             +---------------+
             | Recovery Audit|
             |    Trail      |
             +---------------+
                     |
                     v
             +---------------+
             | PostgreSQL /  |
             |   Supabase    |
             +---------------+
```

---

## 2. Architecture Components

### 2.1 User Layer

Users interact with the application through the browser.

Main activities:

* Registration
* Login
* Payment simulation
* Viewing payment results
* Viewing recovery information
* Monitoring dashboards

---

### 2.2 Presentation Layer

The presentation layer uses:

* HTML5
* CSS3
* Django Templates

It provides the user interface for:

* Home page
* Login
* Registration
* Dashboard
* Payment simulation
* Payment result
* Recovery dashboard
* Audit trail

---

### 2.3 Django Application Layer

Django handles:

* URL routing
* Authentication
* Request processing
* Business logic
* Database operations
* Template rendering
* Security mechanisms

---

## 3. Payment Processing Layer

The payment module creates and manages simulated transactions.

The payment can be:

```text
Successful
    OR
Failed
```

If the payment fails, the failure type is passed to the diagnosis process.

---

## 4. AI Diagnosis Layer

The diagnosis engine is implemented using rule-based logic.

Example:

```text
IF failure_type == "Network Error"
THEN
    diagnosis = "Temporary connectivity issue"
    recommendation = "Retry"
    confidence = "High"
```

Another example:

```text
IF failure_type == "Insufficient Balance"
THEN
    diagnosis = "Insufficient customer balance"
    recommendation = "Customer action required"
```

The rule-based approach makes the decision process explainable.

---

## 5. Safety Layer

Before recovery is performed, the safety layer evaluates the transaction.

Example:

```text
Payment
   |
   v
Amount Check
   |
   +----> Amount > INR 10,000
   |             |
   |             v
   |       Block Recovery
   |
   +----> Safe Amount
                 |
                 v
          Continue Evaluation
```

Additional rules can evaluate:

* Previous recovery attempts
* Failure type
* Transaction amount
* Recovery eligibility

---

## 6. Recovery Layer

If recovery is allowed, the system performs a simulated recovery action.

Possible outcomes:

```text
Recovery Allowed
      |
      v
Simulated Recovery
      |
      v
Recovered / Failed
```

If the guardrail blocks the action:

```text
Recovery Blocked
      |
      v
Blocked Action Recorded
```

---

## 7. Audit Layer

Every important recovery decision can be recorded.

The audit layer provides traceability.

Example:

```text
Payment ID
    +
Failure Type
    +
Diagnosis
    +
Confidence
    +
Recommendation
    +
Safety Decision
    +
Timestamp
```

---

## 8. Database Layer

The production database is PostgreSQL hosted through Supabase.

Main data entities:

```text
User
 |
 +---- Payment
          |
          +---- RecoveryAudit
```

Django's authentication system manages users.

The Payment model stores transaction information.

The RecoveryAudit model stores recovery decision information.

---

## 9. Deployment Architecture

Production deployment follows:

```text
Developer
    |
    v
GitHub Repository
    |
    v
Vercel
    |
    v
Django / Python Application
    |
    v
Supabase PostgreSQL
```

### GitHub

Stores application source code.

### Vercel

Hosts the deployed Django application.

### Supabase

Provides the production PostgreSQL database.

---

## 10. Security Architecture

Security controls include:

```text
User Authentication
        |
        v
Django Authorization
        |
        v
Protected Views
        |
        v
Database Access
```

Additional controls include:

* CSRF protection
* Environment variables
* Secure production configuration
* Admin authentication
* Recovery guardrails
* Audit logging

---

## 11. Complete Workflow

```text
User
 |
 v
Initiate Payment
 |
 v
Payment Processing
 |
 v
Failure Detected
 |
 v
Classify Failure
 |
 v
AI Diagnosis
 |
 v
Confidence Evaluation
 |
 v
Safety Guardrails
 |
 +------------------------+
 |                        |
 v                        v
Allowed                  Blocked
 |                        |
 v                        v
Recovery Simulation    Block Action
 |                        |
 +-----------+------------+
             |
             v
       Audit Logging
             |
             v
        Database
             |
             v
         Dashboard
```

---

## 12. Design Principles

The architecture emphasizes:

* Explainability
* Safety
* Modularity
* Traceability
* Authentication
* Separation of responsibilities
* Controlled automation
* Database persistence

```
```
