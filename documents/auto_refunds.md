# Auto-Refunds Scenarios

This document provides detailed information about scenarios where payments are automatically refunded.

## Common Auto-Refund Scenarios

### 1. Closed QR Code Payments

When a payment is made on a closed QR code, it is automatically refunded.

**Key Points:**
- Payments made on closed QR codes never appear in the merchant dashboard
- Customer sees money debited from their account but merchant doesn't receive it
- System automatically initiates a refund for such payments
- Customer should re-initiate the payment by scanning a valid QR code again

**Example from Tickets:**
- In ticket #14471505, a payment of ₹1690 was auto-refunded (rfnd_Q9JJ0jVMliOkja) because it was made on a closed QR code
- In ticket #14501366, a payment of ₹2803 was auto-refunded (rfnd_QAscdddcnhZHpa) for the same reason

### 2. Payment Not Auto-Captured

When a payment is authorized but not auto-captured, it gets automatically refunded.

**Key Points:**
- This typically happens when the Order API is not implemented
- To prevent this in the future, implement the Order API
- After implementation, payments will be auto-captured and settled according to settlement cycle

**Example from Tickets:**
- In ticket #14475210, a payment of ₹700 was auto-refunded (rfnd_QAdrKI9HqM9L0v) because it was not auto-captured
- In ticket #14471919, a payment of ₹2021 was auto-refunded (rfnd_Q9MlFPRIOeZRaH) for the same reason

### 3. Application Glitches

Sometimes application glitches can lead to duplicate payments, resulting in multiple refunds.

**Key Points:**
- Multiple payments may be created for the same transaction due to app glitches
- Each payment gets its own refund with unique IDs
- Each refund is processed independently with unique RRN/reference numbers

**Example from Tickets:**
- In ticket #14491931, two refunds of ₹950 each (rfnd_QBKty2WMjFKk76 and rfnd_QBKu09YIYXfUXi) were processed due to an application glitch
- In ticket #14496341, two refunds of ₹180 each were processed with unique reference numbers

## Handling Auto-Refunds

### Communication to Customers

When an auto-refund is initiated:

1. Inform the customer about the reason for the auto-refund
2. Provide the Refund ID, Payment ID, and RRN/reference number for tracking
3. Advise that while refunds are processed immediately, banks may take 5-7 working days to credit the amount
4. If appropriate, guide the customer to re-initiate the payment correctly

### Technical Resolution

For merchants experiencing frequent auto-refunds:

1. **Closed QR Code Issues:**
   - Ensure QR codes being used are active and valid
   - Check if there are any configuration issues with QR code generation
   - Monitor QR code status in the dashboard

2. **Auto-Capture Issues:**
   - Implement the Order API following the documentation
   - Ensure proper integration to allow auto-capture of payments
   - Test the implementation to verify payments are captured correctly

## Reference Information

### Relevant API Documentation

For fixing auto-capture issues:
- Order API Documentation: https://razorpay.com/docs/payments/orders/apis

### Common RRN/Reference Number Formats

RRN/Reference numbers typically follow these formats:
- Numeric only (e.g., 508512145411, 508512255794)
- May include alphanumeric characters in some cases 