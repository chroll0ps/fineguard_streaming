from pyspark import pipelines as dp
from pyspark.sql.dataframe import DataFrame
import smtplib
import html
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, body, from_email, app_password):
    """Sends an email using Gmail SMTP server."""
    msg = MIMEMultipart("alternative")
    msg["From"] = f"FinGuard Security <{from_email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(msg)


def create_alert_email_body(alert_data):
    """Creates a wide, white-background Neo-Brutalist HTML email with an Asymmetric Bento layout."""
    amount = float(alert_data['transaction_amount'])
    limit = float(alert_data['transaction_limit'])
    over_limit = max(0.0, amount - limit)

    # Calculate percentages for the clean utilization track and badge
    utilization_pct = int((amount / limit) * 100) if limit > 0 else 100
    if amount > 0 and amount > limit:
        limit_pct = max(12, min(88, int((limit / amount) * 100)))
        over_pct = 100 - limit_pct
    else:
        limit_pct = 100
        over_pct = 0

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FinGuard Transaction Notification</title>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@500;700;800;900&family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet">
</head>
<body style="margin: 0; padding: 0; background-color: #ffffff; font-family: 'Cairo', 'Plus Jakarta Sans', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #141413; -webkit-font-smoothing: antialiased;">

  <!-- Wide Pure White Canvas -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; padding: 40px 20px;">
    <tr>
      <td align="center">

        <!-- Wide 900px Container -->
        <table role="presentation" width="900" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width: 900px; background-color: #ffffff;">

          <!-- ========================================== -->
          <!-- 1. EDITORIAL HEADER                        -->
          <!-- ========================================== -->
          <tr>
            <td align="left" style="padding-bottom: 32px;">
              
              <!-- Top Brand & Alert Status Row -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                <tr>
                  <td align="left" valign="middle">
                    <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td valign="middle" style="padding-right: 10px;">
                          <span style="display: inline-block; width: 28px; height: 11px; background-color: #f5c542; border: 1.5px solid #141413;"></span>
                        </td>
                        <td valign="middle" style="font-size: 13px; font-weight: 800; color: #141413; letter-spacing: 0.4px; text-transform: uppercase;">
                          FinGuard Real-Time Monitoring
                        </td>
                      </tr>
                    </table>
                  </td>
                  <td align="right" valign="middle">
                    <span style="display: inline-block; background-color: #f9f9f8; color: #141413; font-size: 12px; font-weight: 800; padding: 5px 12px; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 3px solid #141413; border-bottom: 3px solid #141413; font-family: monospace;">
                      ALERT #{alert_data['alert_id']}
                    </span>
                  </td>
                </tr>
              </table>

              <!-- Main Headline with Flagship Curved Line Under Customer Name -->
              <h1 style="margin: 0; font-size: 32px; line-height: 1.35; font-weight: 900; color: #141413; letter-spacing: -0.5px;">
                Hi
                <span style="display: inline-block; vertical-align: bottom; text-align: center; padding: 0 4px;">
                  <span style="display: block; line-height: 1.15;">{alert_data['customer_name']}</span>
                  <span style="display: block; height: 8px; border-top: 5px solid #f5c542; border-radius: 50% 50% 0 0 / 100% 100% 0 0; margin-top: 2px;"></span>
                </span>,
                a transaction of <span style="background-color: #f5c542; padding: 0 8px; border: 1.5px solid #141413;">{alert_data['currency']} {amount:,.2f}</span>
              </h1>
              <div style="margin-top: 6px; font-size: 30px; line-height: 1.28; font-weight: 900; color: #141413; letter-spacing: -0.5px;">
                exceeded your configured spending limit
              </div>

            </td>
          </tr>

          <!-- ========================================== -->
          <!-- 2. ASYMMETRIC BENTO GRID                   -->
          <!-- ========================================== -->
          <tr>
            <td style="padding-bottom: 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>

                  <!-- LEFT WIDE SPOTLIGHT (58%): THRESHOLD COMPARISON -->
                  <td width="58%" valign="top" style="background-color: #ffffff; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413; padding: 24px;">
                    
                    <!-- Card Header -->
                    <div style="margin-bottom: 18px;">
                      <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; color: #52524e;">
                        Spending Analysis
                      </div>
                      <div style="font-size: 20px; font-weight: 900; color: #141413;">
                        Threshold Comparison
                      </div>
                    </div>

                    <!-- Split KPI Boxes -->
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 22px;">
                      <tr>
                        <td width="48%" valign="top" style="background-color: #141413; color: #ffffff; padding: 16px 18px; border-right: 5px solid #f5c542; border-bottom: 5px solid #f5c542;">
                          <div style="font-size: 10px; font-weight: 800; color: #f5c542; text-transform: uppercase; letter-spacing: 0.8px;">
                            Transaction Amount
                          </div>
                          <div style="font-size: 22px; font-weight: 900; color: #ffffff; margin-top: 4px;">
                            {alert_data['currency']} {amount:,.2f}
                          </div>
                        </td>
                        <td width="4%">&nbsp;</td>
                        <td width="48%" valign="top" style="background-color: #f9f9f8; color: #141413; padding: 16px 18px; border: 1.5px solid #141413;">
                          <div style="font-size: 10px; font-weight: 800; color: #52524e; text-transform: uppercase; letter-spacing: 0.8px;">
                            Configured Limit
                          </div>
                          <div style="font-size: 22px; font-weight: 900; color: #141413; margin-top: 4px;">
                            {alert_data['currency']} {limit:,.2f}
                          </div>
                        </td>
                      </tr>
                    </table>

                    <!-- Clean & Elegant Limit Utilization Breakdown -->
                    <div style="background-color: #f9f9f8; border: 1.5px solid #e5e4df; padding: 16px 18px;">
                      
                      <!-- Breakdown Header + Utilization Pill -->
                      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 10px;">
                        <tr>
                          <td align="left" valign="middle" style="font-size: 12px; font-weight: 800; color: #141413; text-transform: uppercase; letter-spacing: 0.5px;">
                            Limit Utilization Breakdown
                          </td>
                          <td align="right" valign="middle">
                            <span style="display: inline-block; background-color: #f5c542; color: #141413; font-size: 11px; font-weight: 900; padding: 2px 8px; border: 1px solid #141413;">
                              {utilization_pct}% of Limit
                            </span>
                          </td>
                        </tr>
                      </table>

                      <!-- Sleek Architectural Segmented Bar -->
                      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border: 1.5px solid #141413; background-color: #ffffff; margin-bottom: 12px;">
                        <tr>
                          <td width="{limit_pct}%" style="background-color: #141413; height: 10px; font-size: 0; line-height: 0;">&nbsp;</td>
                          <td width="{over_pct}%" style="background-color: #f5c542; height: 10px; font-size: 0; line-height: 0; border-left: 1.5px solid #141413;">&nbsp;</td>
                        </tr>
                      </table>

                      <!-- Clean Two-Column Legend -->
                      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td align="left" valign="middle" style="font-size: 12px; font-weight: 700; color: #52524e;">
                            <span style="display: inline-block; width: 8px; height: 8px; background-color: #141413; border: 1px solid #141413; margin-right: 6px; vertical-align: middle;"></span>
                            Standard Cap: <strong style="color: #141413;">{alert_data['currency']} {limit:,.2f}</strong>
                          </td>
                          <td align="right" valign="middle" style="font-size: 12px; font-weight: 700; color: #52524e;">
                            <span style="display: inline-block; width: 8px; height: 8px; background-color: #f5c542; border: 1px solid #141413; margin-right: 6px; vertical-align: middle;"></span>
                            Exceeded By: <strong style="color: #141413;">+{alert_data['currency']} {over_limit:,.2f}</strong>
                          </td>
                        </tr>
                      </table>

                    </div>

                  </td>

                  <!-- Middle Spacer -->
                  <td width="2%">&nbsp;</td>

                  <!-- RIGHT STACKED COLUMN (40%): MERCHANT & ORIGIN CARDS -->
                  <td width="40%" valign="top">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                      
                      <!-- HORIZONTAL CARD: MERCHANT PROFILE -->
                      <tr>
                        <td style="background-color: #ffffff; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413; padding: 22px;">
                          <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; color: #52524e; margin-bottom: 2px;">
                            Counterparty
                          </div>
                          <div style="font-size: 17px; font-weight: 900; color: #141413; margin-bottom: 12px;">
                            Merchant Profile
                          </div>

                          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f9f9f8; border-left: 4px solid #f5c542; padding: 14px 16px;">
                            <tr>
                              <td>
                                <div style="font-size: 16px; font-weight: 900; color: #141413;">
                                  {alert_data['merchant_name']}
                                </div>
                                <div style="font-size: 12px; font-weight: 700; color: #52524e; margin-top: 3px;">
                                  Category: <strong style="color: #141413;">{alert_data['merchant_category']}</strong>
                                </div>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>

                      <!-- Vertical Spacer -->
                      <tr>
                        <td height="18" style="font-size: 0; line-height: 0;">&nbsp;</td>
                      </tr>

                      <!-- HORIZONTAL CARD: LOCATION & TIME -->
                      <tr>
                        <td style="background-color: #ffffff; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413; padding: 22px;">
                          <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; color: #52524e; margin-bottom: 2px;">
                            Metadata
                          </div>
                          <div style="font-size: 17px; font-weight: 900; color: #141413; margin-bottom: 12px;">
                            Origin &amp; Timestamp
                          </div>

                          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f9f9f8; border-left: 4px solid #141413; padding: 14px 16px;">
                            <tr>
                              <td>
                                <div style="font-size: 15px; font-weight: 900; color: #141413;">
                                  {alert_data['city']}, {alert_data['country']}
                                </div>
                                <div style="font-size: 12px; font-weight: 700; font-family: monospace; color: #52524e; margin-top: 4px;">
                                  {alert_data['transaction_timestamp']}
                                </div>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>

                    </table>
                  </td>

                </tr>
              </table>
            </td>
          </tr>

          <!-- ========================================== -->
          <!-- 3. WIDE NEO-BRUTALIST STATEMENT TABLE      -->
          <!-- ========================================== -->
          <tr>
            <td style="background-color: #ffffff; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413; padding: 24px 28px;">
              
              <!-- Table Header Row (Number Removed) -->
              <div style="font-size: 20px; font-weight: 900; color: #141413; margin-bottom: 18px;">
                Complete Transaction Breakdown
              </div>

              <!-- Wide Data Table -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border: 1.5px solid #141413; border-collapse: collapse; margin-bottom: 20px;">
                <tr style="background-color: #141413; color: #ffffff;">
                  <th align="left" style="padding: 12px 16px; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; border-right: 1px solid #333333;">
                    Transaction ID
                  </th>
                  <th align="left" style="padding: 12px 16px; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; border-right: 1px solid #333333;">
                    Merchant
                  </th>
                  <th align="left" style="padding: 12px 16px; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; border-right: 1px solid #333333;">
                    Location
                  </th>
                  <th align="left" style="padding: 12px 16px; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; border-right: 1px solid #333333;">
                    Date &amp; Time
                  </th>
                  <th align="right" style="padding: 12px 16px; font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; background-color: #f5c542; color: #141413;">
                    Amount / Limit
                  </th>
                </tr>
                <tr style="background-color: #f9f9f8;">
                  <td style="padding: 14px 16px; font-size: 13px; font-weight: 800; font-family: monospace; color: #141413; border-right: 1px solid #d6d3cd;">
                    {alert_data['transaction_id']}
                  </td>
                  <td style="padding: 14px 16px; font-size: 13px; font-weight: 800; color: #141413; border-right: 1px solid #d6d3cd;">
                    {alert_data['merchant_name']} <span style="font-weight: 500; color: #52524e;">({alert_data['merchant_category']})</span>
                  </td>
                  <td style="padding: 14px 16px; font-size: 13px; font-weight: 700; color: #141413; border-right: 1px solid #d6d3cd;">
                    {alert_data['city']}, {alert_data['country']}
                  </td>
                  <td style="padding: 14px 16px; font-size: 13px; font-weight: 700; font-family: monospace; color: #141413; border-right: 1px solid #d6d3cd;">
                    {alert_data['transaction_timestamp']}
                  </td>
                  <td align="right" style="padding: 14px 16px; font-size: 14px; font-weight: 900; color: #141413; background-color: #fffbeb;">
                    {alert_data['currency']} {amount:,.2f}
                    <div style="font-size: 11px; font-weight: 700; color: #52524e;">
                      Limit: {alert_data['currency']} {limit:,.2f}
                    </div>
                  </td>
                </tr>
              </table>

              <!-- Next Steps Footer Row -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top: 1px solid #d6d3cd; padding-top: 14px;">
                <tr>
                  <td align="left" style="font-size: 13px; font-weight: 700; color: #262625; line-height: 1.6;">
                    <span style="display: inline-block; background-color: #f5c542; padding: 1px 6px; border: 1px solid #141413; font-weight: 900; font-size: 11px; margin-right: 6px;">ACTION</span>
                    If you authorized this transaction, no action is needed. If you need assistance, contact support with Alert ID <strong>{alert_data['alert_id']}</strong>.
                  </td>
                  <td align="right" style="font-size: 13px; font-weight: 900; color: #141413; white-space: nowrap; padding-left: 16px;">
                    FinGuard Monitoring &rarr;
                  </td>
                </tr>
              </table>

            </td>
          </tr>

        </table>
        <!-- End Wide 900px Container -->

      </td>
    </tr>
  </table>

</body>
</html>"""

# Get configuration outside the foreach_batch_sink for serialization
EMAIL_FROM = "<YOUR_SENDER_EMAIL@gmail.com>"
try:
    APP_PASSWORD = dbutils().secrets().get("finguard-scope", "gmail_api_key")
except Exception as e:
    print(f"❌ Failed to retrieve Gmail API key from secrets: {e}")
    APP_PASSWORD = None


@dp.foreach_batch_sink(name="email_notifier_sink")
def send_high_value_alert_emails(df: DataFrame, batch_id: int):
    """ForEachBatch sink that sends email alerts for high-value transactions."""

    if APP_PASSWORD is None:
        print(f"❌ Batch {batch_id}: Gmail API key not available, skipping email notifications")
        return

    rows = df.collect()
    if not rows:
        return

    print(f"📧 Batch {batch_id}: Processing {len(rows)} alert(s)...")

    success_count = 0
    failure_count = 0

    for row in rows:
        try:
            alert_data = {
                "alert_id": row.alert_id,
                "customer_name": row.customer_name,
                "transaction_id": row.transaction_id,
                "transaction_amount": float(row.transaction_amount),
                "currency": row.currency,
                "transaction_limit": float(row.transaction_limit),
                "merchant_name": row.merchant_name,
                "merchant_category": row.merchant_category,
                "transaction_timestamp": str(row.transaction_timestamp),
                "city": row.city,
                "country": row.country,
            }

            subject = (
                f"[FinGuard Security] High-Value Transaction Alert: "
                f"{alert_data['currency']} {alert_data['transaction_amount']:,.2f} at {alert_data['merchant_name']}"
            )
            body = create_alert_email_body(alert_data)

            send_email(row.customer_email, subject, body, EMAIL_FROM, APP_PASSWORD)

            success_count += 1
            print(f"  ✅ Email sent to {row.customer_email} for transaction {row.transaction_id}")

        except Exception as e:
            failure_count += 1
            print(f"  ❌ Error processing alert {row.alert_id}: {e}")

    print(f"📊 Batch {batch_id} complete: {success_count} succeeded, {failure_count} failed")


@dp.append_flow(target="email_notifier_sink")
def high_value_alert_stream():
    """Streaming flow that reads high-value transaction alerts."""
    return spark.readStream.table("fineguard.gold.high_value_transactions_alert")