# AI Payment Failure Recovery Agent

## 📌 Project Description

**AI Payment Failure Recovery Agent** is a Django-based academic web application designed to simulate payment-failure analysis and recovery workflows.

The system simulates payment transactions, identifies possible failure categories, provides a rule-based AI diagnosis with a confidence score, recommends a recovery action, checks the recommendation using predefined safety guardrails, performs a simulated recovery when permitted, and records the complete decision in an audit trail.

> **Important Note:** This project is an educational prototype and simulated environment. It does not process real payments, access real bank accounts, connect to banking systems, or transfer actual money.

---

## 📖 Table of Contents

* [Problem Statement](#-problem-statement)
* [Objectives](#-objectives)
* [Proposed System](#-proposed-system)
* [Why Failure Scenario Is Used](#-why-failure-scenario-is-used)
* [How the System Works](#-how-the-system-works)
* [Failure Scenarios](#-failure-scenarios)
* [AI Diagnosis](#-ai-diagnosis)
* [Safety Guardrails](#-safety-guardrails)
* [Recovery Process](#-recovery-process)
* [Customer Features](#-customer-features)
* [Administrator Features](#-administrator-features)
* [Dashboard](#-dashboard)
* [Recovery Dashboard](#-recovery-dashboard)
* [AI Audit Trail](#-ai-audit-trail)
* [System Architecture](#-system-architecture)
* [Technologies Used](#-technologies-used)
* [Project Structure](#-project-structure)
* [Database Models](#-database-models)
* [URL Routes](#-url-routes)
* [Installation](#-installation)
* [Running the Project](#-running-the-project)
* [Application Workflow](#-application-workflow)
* [Example](#-example)
* [Advantages](#-advantages)
* [Limitations](#-limitations)
* [Future Enhancements](#-future-enhancements)
* [Security](#-security)
* [Academic Purpose](#-academic-purpose)
* [Disclaimer](#-important-disclaimer)
* [Conclusion](#-conclusion)

---

# 🔴 Problem Statement

Payment failures are common in online transactions. When a payment fails, users may receive only a general message such as:

```text
Payment Failed
```

The user may not know:

* Why the payment failed
* Whether the failure is temporary
* What action should be taken
* Whether retrying the payment is appropriate
* Whether the transaction can potentially be recovered

This project demonstrates a system that combines **failure detection, AI-assisted diagnosis, safety guardrails, simulated recovery, revenue tracking, and audit logging** in one application.

---

# 🎯 Objectives

The main objectives are:

* Detect simulated payment failures.
* Identify the possible failure type.
* Determine the likely root cause.
* Provide an AI-based diagnosis.
* Generate a confidence score.
* Recommend an appropriate recovery action.
* Check the recommendation using safety guardrails.
* Prevent unsafe automated recovery.
* Simulate recovery when permitted.
* Calculate simulated recovered revenue.
* Display detailed payment results.
* Provide administrators with recovery statistics.
* Maintain an audit trail of recovery decisions.

---

# 💡 Proposed System

The system follows this process:

```text
Customer
   ↓
Login / Signup
   ↓
Payment Simulation
   ↓
Failure Scenario
   ↓
Failure Detection
   ↓
AI Diagnosis
   ↓
Confidence Score
   ↓
Safety Guardrail
   ↓
Recovery Decision
   ↓
Simulated Recovery
   ↓
Payment Result
   ↓
Audit Trail
```

The system does not automatically retry every failed payment. The recommended action is first evaluated by the safety guardrail.

---

# ❓ Why Failure Scenario Is Used

### Important Explanation

The **Failure Scenario** option is included because this project is currently a **simulated payment environment**.

In a real payment application, customers would **not normally select or enter the reason for their own payment failure**.

A real payment system would work approximately like this:

```text
Customer
   ↓
Makes Payment
   ↓
Payment Gateway
   ↓
Transaction Processing
   ↓
Payment Fails
   ↓
Gateway Returns Failure Information
   ↓
AI Payment Failure Recovery Agent
```

For example, a real payment gateway could return information indicating:

```text
Payment Timeout
```

or:

```text
Bank Error
```

or:

```text
Insufficient Balance
```

However, this academic project does not connect to a real payment gateway or banking system.

Therefore, the **Failure Scenario** field is used as a **testing and demonstration mechanism**.

It allows the project evaluator or developer to intentionally simulate different payment failures and verify that the system responds correctly.

For example, selecting:

```text
Bank Error
```

allows the system to demonstrate:

```text
Bank Error
     ↓
Failure Detection
     ↓
AI Diagnosis
     ↓
88% Confidence
     ↓
Retry Payment
     ↓
Safety Check
     ↓
Approved
     ↓
Simulated Recovery
```

Similarly, selecting:

```text
Insufficient Balance
```

allows the system to demonstrate a different diagnosis and recovery recommendation.

### Why this is useful for the academic project

Without the Failure Scenario option, it would be difficult to reliably demonstrate every failure condition because the project does not have a real payment gateway generating actual failures.

The option therefore allows controlled testing of:

* Failure detection
* AI diagnosis
* Confidence scoring
* Recovery recommendations
* Safety policies
* Recovery execution
* Audit logging

### Real-world implementation

In a future production implementation, the customer would not select the failure scenario.

Instead, the payment gateway would automatically provide the failure information:

```text
Real Payment
     ↓
Payment Gateway
     ↓
Failure Response
     ↓
Failure Detection
     ↓
AI Diagnosis
     ↓
Safety Guardrail
     ↓
Recovery Decision
```

Therefore, the Failure Scenario field is **only used for simulation and testing in the current academic version**.

---

# ⚙️ How the System Works

## 1. User Registration

A new customer can create an account using:

* Username
* Password
* Confirm Password

The project uses Django's built-in authentication system.

---

## 2. User Login

Registered users can log in using their credentials.

After successful authentication, the user is redirected to the dashboard.

---

## 3. Dashboard

The dashboard displays:

* Total payments
* Failed payments
* Revenue recovered
* Revenue at risk
* Recovery rate
* Payment history

Administrators additionally have access to:

* Make a Payment
* Recovery Dashboard
* AI Audit Trail

---

# 💳 Payment Simulation

The **Make a Payment** page allows the user to create a simulated payment.

Example:

```text
Amount: ₹420
Payment Method: UPI
Bank: State Bank of India
Failure Scenario: Bank Error
```

The system then processes the simulated transaction through its failure analysis and recovery workflow.

---

# 🚨 Failure Scenarios

The current system supports the following simulated scenarios:

| Failure Scenario        | Possible Cause                                |
| ----------------------- | --------------------------------------------- |
| Payment Timeout         | Temporary gateway or network timeout          |
| Network Error           | Network communication problem                 |
| Insufficient Balance    | Insufficient available funds                  |
| Payment Declined        | Bank or gateway declined the transaction      |
| Bank Error              | Temporary bank-side processing problem        |
| UPI Failure             | UPI or bank-side transaction problem          |
| Gateway Server Error    | Payment gateway server problem                |
| Invalid Payment Details | Incorrect or incomplete payment information   |
| Authentication Failure  | Payment authentication could not be completed |

---

# 🤖 AI Diagnosis

The project uses a **rule-based AI diagnosis engine**.

Based on the detected failure type, it generates:

1. AI Diagnosis
2. Confidence Score
3. Recommended Recovery Action

Example:

```text
Failure Type:
Bank Error

AI Diagnosis:
The bank appears to have encountered a temporary
processing problem.

AI Confidence:
88%

Recovery Action:
Retry payment
```

The current AI implementation is rule-based and intended for academic demonstration.

---

# 🛡️ Safety Guardrails

Before executing recovery, the recommended action is checked by the safety guardrail.

Approved actions include:

```text
Retry payment
Request customer to use another payment method
Request customer to correct payment details
Request customer authentication
```

---

## High-Value Transaction Protection

If the simulated payment amount is greater than:

```text
₹10,000
```

the system blocks automatic recovery and requires manual review.

Example:

```text
Risk Level:
HIGH

Policy Action:
Manual review required

Decision:
Recovery Blocked
```

This demonstrates that the recovery agent does not blindly execute every recommended action.

---

# 🔄 Recovery Process

If the safety guardrail approves the recommended action, the system performs a **simulated recovery**.

Example:

```text
Failure:
Bank Error

      ↓

AI Recommendation:
Retry Payment

      ↓

Safety Guardrail:
Approved

      ↓

Simulated Recovery:
Executed

      ↓

Status:
RECOVERED
```

If customer intervention is required:

```text
Status:
FAILED

Recovery Result:
Customer action required before recovery.
```

---

# 👤 Customer Features

Customers can:

* Register
* Login
* Logout
* View their dashboard
* Make simulated payments
* Select failure scenarios for testing
* View payment history
* View failure reasons
* View failure types
* View AI diagnosis
* View AI confidence
* View recovery recommendations
* View recovery results
* View recovered revenue
* View individual payment details

Customers can only access payments associated with their own account.

---

# 👨‍💼 Administrator Features

Administrators can:

* Login
* View all payments
* Access Recovery Dashboard
* Monitor failed payments
* Monitor recovered payments
* View revenue recovered
* View revenue at risk
* View recovery rate
* View blocked recovery actions
* View failure-type distribution
* Access AI Audit Trail

---

# 📊 Dashboard

The main dashboard displays:

```text
Total Payments
Failed Payments
Revenue Recovered
Revenue at Risk
Recovery Rate
```

Payment history includes:

```text
Payment ID
Order ID
Amount
Payment Method
Bank
Failure Reason
Status
Recovery Action
Payment Details
```

---

# 📈 Recovery Dashboard

The administrator Recovery Dashboard provides overall recovery statistics:

```text
Total Payments
Recovered Payments
Failed Payments
Blocked Actions
Revenue Recovered
Recovery Rate
```

It also displays the distribution of payment failure types.

Example:

```text
Total Payments:       20
Recovered Payments:   12
Failed Payments:       8
Blocked Actions:       2
Revenue Recovered: ₹5,400
Recovery Rate:        60%
```

The displayed values depend on the simulated transactions created in the application.

---

# 🔍 AI Audit Trail

The AI Audit Trail records the recovery decision-making process.

It stores information such as:

```text
Payment
Failure Type
Root Cause
Recommended Action
AI Confidence
Policy Action
Allowed / Blocked
Risk Level
Executed
Recovery Result
Safety Reason
```

Example:

```text
Failure Type:
Bank Error

Root Cause:
The bank was unable to process the transaction.

Recommended Action:
Retry payment

AI Confidence:
88%

Risk Level:
LOW

Policy Decision:
Allowed

Execution:
Executed

Result:
Simulated retry executed successfully
```

This provides transparency into the recovery process.

---

# 🏗️ System Architecture

```text
┌──────────────────────────────────────────────┐
│                 USER LAYER                   │
│          Customers • Administrators          │
└───────────────────────┬──────────────────────┘
                        ↓
┌──────────────────────────────────────────────┐
│             AUTHENTICATION LAYER             │
│            Login • Signup • Logout           │
└───────────────────────┬──────────────────────┘
                        ↓
┌──────────────────────────────────────────────┐
│               PAYMENT LAYER                  │
│           Simulated Payment Processing       │
└───────────────────────┬──────────────────────┘
                        ↓
┌──────────────────────────────────────────────┐
│          FAILURE DETECTION LAYER             │
│          Failure Type Identification         │
└───────────────────────┬──────────────────────┘
                        ↓
┌──────────────────────────────────────────────┐
│              AI DIAGNOSIS LAYER              │
│       Diagnosis • Confidence • Action         │
└───────────────────────┬──────────────────────┘
                        ↓
┌──────────────────────────────────────────────┐
│             SAFETY GUARDRAIL LAYER           │
│          Risk Analysis • Policy Check        │
└───────────────────────┬──────────────────────┘
                        ↓
┌──────────────────────────────────────────────┐
│               RECOVERY LAYER                 │
│             Simulated Recovery               │
└───────────────────────┬──────────────────────┘
                        ↓
┌──────────────────────────────────────────────┐
│                AUDIT LAYER                   │
│         Recovery Decision Tracking           │
└──────────────────────────────────────────────┘
```

---

# 🧰 Technologies Used

## Backend

* Python
* Django 4.2.1

## Frontend

* HTML5
* CSS3
* JavaScript
* Django Templates

## Database

* SQLite for the current development environment
* MySQL can be configured for future deployment

## Authentication

* Django Authentication System
* Django Sessions
* Staff/Admin authorization

---

# 📁 Project Structure

```text
Payment-Failure-Recovery-Agent/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── payment_recovery/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── payments/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── tests.py
    │
    ├── migrations/
    │   ├── __init__.py
    │   └── ...
    │
    └── templates/
        ├── registration/
        │   ├── login.html
        │   └── signup.html
        │
        └── payments/
            ├── dashboard.html
            ├── make_payment.html
            ├── payment_result.html
            ├── recovery_dashboard.html
            └── audit_trail.html
```

If a separate static directory is used:

```text
static/
└── css/
    └── style.css
```

---

# 🗄️ Database Models

## Payment

The `Payment` model stores:

```text
User
Payment ID
Order ID
Amount
Payment Method
Bank
Failure Type
Failure Reason
Cancellation Reason
Status
Retry Count
AI Diagnosis
AI Confidence
Recovery Action
Recovery Result
Revenue Recovered
Created At
```

## RecoveryAudit

The `RecoveryAudit` model stores:

```text
Payment
Failure Type
Cancellation Reason
Root Cause
Recommended Action
Confidence
Policy Action
Allowed
Risk Level
Executed
Result
Reason
Created At
```

---

# 🌐 URL Routes

| URL                             | Purpose                          |
| ------------------------------- | -------------------------------- |
| `/`                             | Home/Dashboard                   |
| `/login/`                       | User Login                       |
| `/signup/`                      | User Registration                |
| `/register/`                    | Registration Compatibility Route |
| `/logout/`                      | Logout                           |
| `/dashboard/`                   | Payment Dashboard                |
| `/make-payment/`                | Simulated Payment                |
| `/payment-result/<payment_id>/` | Payment Result                   |
| `/recovery-dashboard/`          | Admin Recovery Dashboard         |
| `/audit-trail/`                 | Admin AI Audit Trail             |

---

# 📦 Requirements

The main dependencies are listed in `requirements.txt`.

Example:

```text
Django==4.2.1
PyMySQL==1.1.1
```

Install them using:

```bash
pip install -r requirements.txt
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
```

## 2. Open the Project

```bash
cd Payment-Failure-Recovery-Agent
```

## 3. Create Virtual Environment

```bash
python -m venv venv
```

## 4. Activate Virtual Environment

### Windows

```powershell
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

## 5. Install Requirements

```bash
pip install -r requirements.txt
```

## 6. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 7. Create Administrator

```bash
python manage.py createsuperuser
```

Follow the instructions displayed in the terminal.

---

# ▶️ Running the Project

Start the Django development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🔁 Complete Application Workflow

```text
1. Register Account
        ↓
2. Login
        ↓
3. Open Dashboard
        ↓
4. Make Simulated Payment
        ↓
5. Select Failure Scenario
        ↓
6. Detect Failure
        ↓
7. Generate AI Diagnosis
        ↓
8. Calculate Confidence
        ↓
9. Recommend Recovery Action
        ↓
10. Apply Safety Guardrail
        ↓
11. Approve or Block Action
        ↓
12. Simulate Recovery
        ↓
13. Display Payment Result
        ↓
14. Record Audit Trail
        ↓
15. Administrator Monitors Recovery
```

---

# 🧪 Example

Consider this simulated transaction:

```text
Amount:
₹420

Payment Method:
UPI

Bank:
State Bank of India

Failure Scenario:
Bank Error
```

The system can produce:

```text
Failure Type:
Bank Error

AI Diagnosis:
The bank appears to have encountered a temporary
processing problem.

AI Confidence:
88%

Recovery Action:
Retry payment

Risk Level:
LOW

Safety Decision:
Approved

Recovery Result:
Simulated retry executed successfully

Payment Status:
RECOVERED

Revenue Recovered:
₹420
```

The complete decision is recorded in the AI Audit Trail.

---

# 🔐 Security

The application uses Django's authentication and authorization features.

Security-related features include:

* User authentication
* Login protection
* Logout
* Django session management
* Staff/admin authorization
* Customer-specific payment access
* Protected Recovery Dashboard
* Protected AI Audit Trail

Customers can only view their own payment information, while administrators can access overall payment and recovery information.

---

# ✅ Advantages

* Provides detailed payment failure analysis.
* Explains possible causes of payment failures.
* Provides an AI confidence score.
* Recommends suitable recovery actions.
* Uses safety guardrails before recovery.
* Blocks high-value transactions from automatic recovery.
* Simulates recovery safely.
* Tracks simulated recovered revenue.
* Provides customer-specific payment history.
* Provides administrator analytics.
* Maintains a complete audit trail.
* Suitable for academic demonstration and testing.
* Can be extended with real payment gateway integrations.

---

# ⚠️ Limitations

The current implementation is an academic prototype.

Therefore:

* It does not process real payments.
* It does not connect to real banks.
* It does not access customer bank accounts.
* It does not transfer actual money.
* Recovery actions are simulated.
* The AI diagnosis is rule-based.
* Failure scenarios are manually selected for simulation.
* It is not intended for production financial use.

---

# 🔮 Future Enhancements

Possible future improvements include:

* Real payment gateway integration
* Automatic gateway failure-response processing
* Machine-learning-based failure prediction
* Real-time payment monitoring
* Advanced fraud detection
* Transaction anomaly detection
* Email notifications
* SMS notifications
* Advanced recovery strategies
* Payment gateway APIs
* REST API integration
* Cloud deployment
* Advanced administrator analytics
* Machine-learning models trained on historical payment data

In a future real-world implementation, the Failure Scenario field would be removed from the customer-facing payment form. Failure information would instead be received automatically from the payment gateway.

---

# 🏭 Future Real-World Workflow

### Current Academic Version

```text
Customer
   ↓
Simulated Payment
   ↓
Select Failure Scenario
   ↓
AI Analysis
   ↓
Safety Guardrail
   ↓
Simulated Recovery
```

### Possible Future Production Version

```text
Customer
   ↓
Real Payment
   ↓
Payment Gateway
   ↓
Payment Failure Response
   ↓
Failure Detection
   ↓
AI Diagnosis
   ↓
Safety Guardrail
   ↓
Recovery Decision
   ↓
Approved Recovery / Manual Review
   ↓
Customer Notification
   ↓
Audit Trail
```

The customer would not manually provide the failure reason in the future production version.

---

# 🎓 Academic Purpose

This project demonstrates the integration of:

* Web application development
* Django framework
* User authentication
* Database management
* Rule-based AI
* Failure analysis
* Decision-making
* Safety guardrails
* Recovery simulation
* Revenue tracking
* Audit logging
* Role-based access control

The project demonstrates how these technologies can be combined into a structured payment-failure analysis and recovery workflow.

---

# 📌 Important Note

**The Failure Scenario field is intentionally included only because the current application is a simulated academic environment.**

It provides a controlled way to reproduce different failure conditions and demonstrate the complete AI recovery workflow without connecting to real payment gateways or financial systems.

In a real-world implementation, failure information would be obtained automatically from the payment gateway rather than being selected by the customer.

---

# ⚠️ Important Disclaimer

> **This project is developed strictly for educational, academic, testing, and demonstration purposes. It uses simulated payment transactions and simulated recovery actions. It does not process real financial transactions, access real bank accounts, transfer actual money, or provide real financial advice. It should not be used as a production payment or banking system without appropriate security, compliance, payment-gateway integration, testing, and professional review.**

---

# 🏁 Conclusion

The **AI Payment Failure Recovery Agent** demonstrates a complete simulated workflow for handling failed payment transactions.

Instead of simply displaying:

```text
Payment Failed
```

the system provides:

```text
Failure Reason
      ↓
Failure Type
      ↓
Root Cause
      ↓
AI Diagnosis
      ↓
Confidence Score
      ↓
Recovery Recommendation
      ↓
Safety Decision
      ↓
Recovery Result
      ↓
Audit Trail
```
