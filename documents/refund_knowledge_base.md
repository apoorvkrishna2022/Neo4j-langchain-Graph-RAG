# Refund Knowledge Repository

This knowledge base contains comprehensive information about payment refunds, including types, processes, common scenarios, and troubleshooting steps.

## Table of Contents

1. [Refund Types](#refund-types)
2. [Refund States](#refund-states)
3. [Refund Timelines](#refund-timelines)
4. [Common Scenarios](#common-scenarios)
5. [Troubleshooting Steps](#troubleshooting-steps)
6. [Required User Data](#required-user-data)

## Refund Types

### Normal Refund
- Amount is refunded within 5-7 working days
- No additional charges are applied
- This is the default refund type

### Instant Refund
- Amount is refunded almost immediately
- A small fee is charged for instant refunds
- Available for specific payment methods (netbanking and UPI)
- Provides better user experience and improves customer trust

### Batch Refund
- Issue refunds in bulk using an XLSX or CSV file
- File is processed after 70 minutes of upload
- Can be canceled within 70 minutes before processing

## Refund States

### Created
- The refund is initiated from the system
- This state is displayed only on the Refunds API

### Processed
- This is the final state of a successful refund
- Indicates the refund has been processed on the system side
- Bank may still take 5-7 working days to credit the amount

### Failed
- A refund can fail due to various reasons:
  - Normal refunds are not possible for payments more than 6 months old
  - Instant refunds can fail due to customer's account or bank-related issues

## Refund Timelines

- Normal refunds: 5-7 working days
- Instant refunds: Almost immediate
- Bank crediting time: Even after a refund is marked as "processed", banks may take 5-7 working days to credit the amount to the customer's account

## Common Scenarios

### Auto-Refunds
1. **Closed QR Code**: Payments made on a closed QR code are automatically refunded. The customer should re-initiate the payment by scanning the QR code again.

2. **Payment Not Auto-Captured**: When a payment is not auto-captured, it gets auto-refunded. To prevent this, implement the order API which ensures payments are auto-captured and settled according to the settlement cycle.

### Multiple Refunds
- In some cases, duplicate payments may occur due to application glitches, resulting in multiple refunds
- Each refund has a unique Refund ID, Payment ID, and RRN/reference number

### Refund Tracking
- Every refund has a unique identifier (Refund ID)
- RRN (Razorpay Reference Number) or ARN (Application Reference Number) is provided to track the refund with the bank
- For UPI payments, the reference number is referred to as RRN
- For other payment methods, it's referred to as ARN or UTR (Unique Transfer Reference)

## Troubleshooting Steps

### When Customer Claims Refund Not Received
1. Verify if the refund has been processed in the system
2. Check the refund status using the Refund ID or Payment ID
3. Provide the customer with the RRN/ARN/UTR number to track with their bank
4. Advise the customer to wait for 5-7 working days for the amount to be credited

### When Bank Fails to Recognize Transaction
1. Customer should contact their bank's Dispute/Chargeback Department
2. Raise a dispute regarding the transaction
3. Submit a copy of the bank statement as proof of debit with the statement: "Money has been debited from my account and I have not received any services or refund"

### Low Account Balance
- If current balance is less than the refund amount:
  - Wait for further payments to be received
  - Add funds to the account from the Dashboard

## Required User Data

To effectively handle refund queries, the following data points are necessary:

1. **Refund Identification**:
   - Refund ID (e.g., rfnd_QBKty2WMjFKk76)
   - Payment ID (e.g., pay_Q4XsbEEaqMly83)
   - Transaction date

2. **Payment Details**:
   - Amount
   - Payment method (UPI, netbanking, card, etc.)
   - Currency

3. **Reference Numbers**:
   - RRN (Razorpay Reference Number) for UPI transactions
   - ARN (Application Reference Number) for card transactions
   - UTR (Unique Transfer Reference) for specific bank transfers

4. **Merchant Information**:
   - Merchant ID
   - Store ID (if applicable)
   - Device ID (if applicable)

5. **Customer Information**:
   - Bank account details (for tracking refunds)
   - Bank statement (for dispute resolution)
   - Contact information for follow-up 