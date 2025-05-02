# Refund Fees, Charges and Business Policies

This document provides information about fees, charges, and business policies related to refunds.

## Refund Fees

### Normal Refunds

- No charges are applied for normal refunds
- The refund is processed within 5-7 working days
- While the refund itself is free, fees and taxes charged for the original captured payment are not reversed
- This is the default refund method if no speed is specified

### Instant Refunds

- A small fee is charged for instant refunds
- The platform fee charged on the original transaction is not refunded
- The instant refund fee varies based on payment methods and merchant agreement
- Instant refunds provide a better customer experience and build trust

## Refund Policies

### Source Refunds

- For prevention of chargebacks, only **source refunds** are processed
- Money is refunded to the same payment method that the customer used to make the payment
- Examples:
  - Credit card payments are refunded to the same credit card
  - UPI payments are refunded to the same VPA used for payment

### Refund Limitations

1. **Time Limitations**:
   - Normal refunds are not possible for payments which are more than 6 months old
   - Refund requests for older payments may need special processing

2. **Amount Limitations**:
   - Full refund: The entire payment amount is refunded
   - Partial refund: Only a portion of the payment amount is refunded
   - The refund amount cannot exceed the original payment amount

3. **Irrevocable Nature**:
   - Once a refund is issued, it cannot be canceled or reversed
   - All refund decisions should be made carefully before initiation

### Account Balance Requirements

- The merchant's account must have sufficient balance to process refunds
- If the balance is insufficient, the merchant can:
  - Wait for further payments to increase the balance
  - Add funds to the account manually from the Dashboard

## Payment Method-Specific Policies

### UPI Refunds

- Refunds to UPI are tracked using RRN (Razorpay Reference Number)
- Instant refunds are available for UPI transactions
- The money is refunded to the same VPA that was used for the payment

### Card Refunds

- Refunds to cards are tracked using ARN (Application Reference Number)
- Processing time depends on the issuing bank
- The refund is credited to the same card that was used for payment

### Netbanking Refunds

- Refunds to netbanking are tracked using UTR (Unique Transfer Reference)
- Instant refunds are available for netbanking transactions
- The refund is credited to the same bank account that was used for payment

## International Refund Policies

- Instant refunds are available for payments involving international currencies
- The refund is processed in the same currency as the original payment
- Additional processing time may be required for international refunds

## Chargeback Handling

If a chargeback is received for an instantly refunded payment:

- The processed refund will have a UTR (Unique Transfer Reference) in the callback
- The UTR appears against the ARN parameter in the Refund entity
- The UTR serves as proof of completed refund between merchant and payment processor
- The RRN of the payment is passed in the Fund Transfer Request for the refund
- This ties the instant refund back to the parent payment, serving as proof of refund
- This data can be used as a defense against future chargeback or arbitration cases

## Business Practices Derived from Tickets

### Auto-Refund Scenarios

The system automatically refunds payments in certain scenarios:

1. **Closed QR Code Payments**
   - When payment is made on a closed QR code, it's automatically refunded
   - The customer should re-initiate the payment by scanning a valid QR code

2. **Non-Auto-Captured Payments**
   - If a payment is not auto-captured, it gets auto-refunded
   - To prevent this, merchants should implement the Order API

### Communication Practices

When handling refund inquiries:

1. **Provide Complete Information**
   - Include Refund ID, Payment ID, and RRN/reference number
   - Specify the refund amount and processing date
   - Explain the current status of the refund

2. **Set Clear Expectations**
   - Inform that banks may take 5-7 working days to credit the amount
   - Explain that tracking is possible with the reference number
   - Advise on next steps if the refund is not received

3. **Bank Dispute Guidance**
   - If the bank fails to recognize the transaction, advise the customer to:
     - Contact their bank's Dispute/Chargeback Department
     - Raise a dispute with evidence of the debit
     - Provide necessary documentation

### Multiple Refunds Handling

When multiple refunds are processed for the same transaction:

- Clearly explain why multiple refunds were processed
- Provide tracking information for each refund
- Ensure the customer understands that all amounts will be refunded 