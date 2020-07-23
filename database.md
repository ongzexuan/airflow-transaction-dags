# Database Fields

Here we document the database fields, what they refer to, and the data type of each field. Note we do not add pending transactions to the database.

| field | data type | about |
| --- | --- | --- |
| `transaction_id` | `text` | Unique transaction ID from Plaid. |
| `pending_transaction_id` | `text` | Unique pending transaction ID from Plaid, if it exists. |
| `account_id` | `text` | Account associated with the transaction. Separate file maps `account_id`s to names. |
| `name` | `text` | Item transacted, name of transaction. |
| `amount` | `real` | Currency amount. Positive amount indicates debit, negative amount indicates credit. |
| `category_id` | `integer` | Category ID, not sure obtained from where. |
| `category` | `text []` | List of category labels for transaction. |
| `date` | `date` | Date of transaction. |
| `iso_currency_code` | `varchar(3)` | ISO currency code of transaction. We assume default to be USD. |
| `location` | `json` | Location of transaction, as a `jsonb` object, containing the fields: `address`, `city`, `country`, `lat`, `lon`, `postal_code`, `region`, `store_number`    . |
| `payment_channel` | `text` | As far as I know, whether transaction was in store or online. |
| `transaction_type` | `text` | Similar to `payment_channel`, but seems to be labeled slightly differently. |
| `pending` | `boolean` | Whether transaction is pending or not. |
| `payment_reference` | `text` | Payment reference ID, if it exists. |
| `merchant` | `text` | (Generated item) Merchant / seller, generated from name, if possible. |
