# Refund Tracking and Troubleshooting

This document provides detailed information about how to track refunds and troubleshoot common issues.

## Refund Tracking Information

### Reference Numbers

Every processed refund has a reference number that can be used to track the refund with the bank:

1. **RRN (Razorpay Reference Number)**: Used for UPI transactions
   - Example: 508512145411, 508512255794

2. **ARN (Application Reference Number)**: Used for card transactions
   - Example: 127097404198

3. **UTR (Unique Transfer Reference)**: Used for specific bank transfers
   - Example: 02705605039037920208383

These reference numbers are essential for tracking refunds with the issuing bank when customers report not receiving the refund.

### Refund States and What They Mean

#### Created
- Initial state when the refund is initiated
- Visible only on the Refunds API

#### Processed
- Indicates the refund has been successfully processed on the system side
- The refund has been initiated through the banking network
- **Important**: This does not guarantee that the customer has received the money in their account

#### Failed
- The refund couldn't be processed due to various reasons
- Common causes include:
  - Payment is older than 6 months (for normal refunds)
  - Customer's bank/account issues (for instant refunds)

## Troubleshooting Common Refund Issues

### 1. Customer Claims Refund Not Received

**Steps to Resolve:**

1. **Verify Refund Status**:
   - Check if the refund is in "processed" state
   - Confirm the refund amount matches the expected amount
   - Verify when the refund was processed

2. **Provide Tracking Information**:
   - Share the RRN/ARN/UTR with the customer
   - Example: "Your refund with Refund ID rfnd_QBKty2WMjFKk76 and reference number 508512145411 was processed on 26 Mar 2025"

3. **Manage Expectations**:
   - Inform that while refunds are processed immediately from the system, banks may take 5-7 working days to credit the amount
   - Ask the customer to check with their bank after 7 working days if the amount is still not credited

**Example from Tickets:**
- In ticket #14491931, the merchant was provided with specific refund IDs, amounts, payment IDs, and reference numbers to track two refunds of ₹950 each

### 2. Bank Does Not Recognize the Transaction

If the customer's bank fails to recognize the transaction even after providing the reference number:

1. **Customer Actions**:
   - Contact their bank's Dispute/Chargeback Department
   - Raise a dispute regarding the transaction
   - Submit a copy of their bank statement as proof of debit with the statement: "Money has been debited from my account and I have not received any services or refund"

2. **Merchant Support**:
   - Provide all necessary transaction details to help the customer with their dispute
   - Maintain records of the refund initiation and processing

### 3. Unable to Initiate Refund Due to Low Balance

If a merchant is unable to initiate a refund due to insufficient balance:

1. **Options for Merchants**:
   - Wait for further payments to be received to increase the balance
   - Add funds to the account manually from the Dashboard

### 4. Multiple Refunds for Same Transaction

If multiple refunds are showing for the same transaction:

1. **Verification Steps**:
   - Check if there were multiple payment attempts by the customer
   - Verify each refund has a unique Refund ID and Payment ID
   - Confirm if the issue was due to an application glitch

2. **Communication with Customer**:
   - Explain the situation clearly, mentioning all refund IDs and reference numbers
   - Assure the customer that all amounts will be refunded to their original payment source

**Example from Tickets:**
- In ticket #14496341, two refunds of ₹180 each were processed with unique reference numbers (508516889975 and 508516430053)

## Time-Based Issues

### 1. Recent Refunds (Less than 7 days)

For refunds processed recently:
- Advise the customer to wait for the full 5-7 working day period
- Provide the reference number for tracking with their bank

### 2. Older Refunds (More than 7 days)

For refunds processed more than 7 working days ago:
- Verify if the refund was actually processed (not just initiated)
- Suggest the customer contact their bank with the reference number
- If the bank cannot locate the transaction, recommend filing a dispute

### 3. Very Old Payments (More than 6 months)

For payments older than 6 months:
- Normal refunds may not be possible
- Special processing might be required
- Escalate to the appropriate team for resolution

## Escalation Process

For unresolved refund issues:

1. **When to Escalate**:
   - Refund is in "processed" state for more than 7 working days but not received by customer
   - Bank is unable to trace the refund using the provided reference number
   - Refund is showing "failed" status without a clear reason

2. **Information Required for Escalation**:
   - Refund ID
   - Payment ID
   - Transaction date
   - RRN/ARN/UTR number
   - Customer contact information
   - Bank statement (if available)

**Example from Tickets:**
- In ticket #14316663, a refund issue was escalated to tech and business teams with reference number 14316663 