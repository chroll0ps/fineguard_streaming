from pyspark import pipelines as dp
from pyspark.sql.dataframe import DataFrame
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, body, from_email, app_password):
    """Sends an email using Gmail SMTP server."""
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_email, app_password)
        server.send_message(msg)


def create_fraud_alert_email_body(alert_data):
    """Creates a wide Neo-Brutalist HTML email body for a fraud card alert."""
    amount = float(alert_data['amount'])
    intl_label = "Yes (Cross-Border)" if alert_data['is_international'] else "No (Domestic)"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FinGuard Fraud Security Alert</title>
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
          <!-- 1. HERO HEADER WITH STANDALONE GREETING    -->
          <!-- ========================================== -->
          <tr>
            <td align="left" style="padding-bottom: 28px;">
              
              <!-- Top Kicker & Alert Metadata Row -->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 22px;">
                <tr>
                  <td align="left" valign="middle">
                    <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td valign="middle" style="padding-right: 10px;">
                          <span style="display: inline-block; width: 28px; height: 11px; background-color: #ff5c5c; border: 1.5px solid #141413;"></span>
                        </td>
                        <td valign="middle" style="font-size: 13px; font-weight: 900; color: #141413; letter-spacing: 0.5px; text-transform: uppercase;">
                          FinGuard Security Watchlist Match
                        </td>
                      </tr>
                    </table>
                  </td>
                  <td align="right" valign="middle">
                    <span style="display: inline-block; background-color: #f5c542; color: #141413; font-size: 12px; font-weight: 900; padding: 5px 12px; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 3px solid #141413; border-bottom: 3px solid #141413; font-family: monospace;">
                      CASE #{alert_data['alert_id']}
                    </span>
                  </td>
                </tr>
              </table>

              <div style="margin-bottom: 14px; font-size: 30px; font-weight: 900; color: #141413; letter-spacing: -0.4px; line-height: 1.2;">
                Hi
                <span style="display: inline-block; vertical-align: bottom; text-align: center; padding: 0 4px;">
                  <span style="display: block; line-height: 1.1;">{alert_data['customer_name']}</span>
                  <span style="display: block; height: 8px; border-top: 5px solid #f5c542; border-radius: 50% 50% 0 0 / 100% 100% 0 0; margin-top: 3px;"></span>
                </span>,
              </div>

              <!-- Main Urgent Headline -->
              <h1 style="margin: 0; font-size: 34px; line-height: 1.25; font-weight: 900; color: #141413; letter-spacing: -0.6px;">
                Suspicious activity was detected on card <span style="background-color: #ff5c5c; color: #ffffff; padding: 0 10px; border: 1.5px solid #141413; font-family: monospace;">****{alert_data['card_number_masked']}</span>
              </h1>
              <p style="margin: 10px 0 0 0; font-size: 15px; font-weight: 700; color: #52524e;">
                Our real-time risk engine matched this transaction against an active security watchlist record.
              </p>

            </td>
          </tr>

          <!-- ========================================== -->
          <!-- 2. FULL-WIDTH INCIDENT COMMAND BANNER      -->
          <!-- ========================================== -->
          <tr>
            <td style="padding-bottom: 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #141413; color: #ffffff; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 5px solid #f5c542; border-bottom: 5px solid #f5c542; padding: 24px 28px;">
                <tr>
                  <td>
                    <!-- Top Row: 3 Classification Badges + Required Action -->
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 18px; border-bottom: 1px solid #333330; padding-bottom: 16px;">
                      <tr>
                        <td align="left" valign="middle">
                          <span style="display: inline-block; background-color: #ff5c5c; color: #141413; font-size: 11px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.6px; padding: 4px 10px; border: 1.5px solid #ffffff; margin-right: 8px;">
                            Risk: {alert_data['risk_level']}
                          </span>
                          <span style="display: inline-block; background-color: #262625; color: #f5c542; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; padding: 4px 10px; border: 1px solid #52524e; margin-right: 8px;">
                            Type: {alert_data['alert_type']}
                          </span>
                          <span style="display: inline-block; background-color: #262625; color: #ffffff; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; padding: 4px 10px; border: 1px solid #52524e;">
                            Watchlist: {alert_data['watch_type']}
                          </span>
                        </td>
                        <td align="right" valign="middle">
                          <span style="font-size: 11px; font-weight: 800; color: #a3a39e; text-transform: uppercase; letter-spacing: 0.6px; margin-right: 6px;">
                            System Directive:
                          </span>
                          <span style="display: inline-block; background-color: #f5c542; color: #141413; font-size: 12px; font-weight: 900; text-transform: uppercase; padding: 4px 12px; border: 1.5px solid #ffffff;">
                            {alert_data['action']}
                          </span>
                        </td>
                      </tr>
                    </table>

                    <!-- Bottom Row: Watchlist Trigger Reason -->
                    <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; color: #f5c542; margin-bottom: 4px;">
                      Trigger Reason &amp; Security Assessment
                    </div>
                    <div style="font-size: 16px; font-weight: 800; color: #ffffff; line-height: 1.5;">
                      {alert_data['reason_description']}
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- ========================================== -->
          <!-- 3. SPLIT DOSSIER: CARD VISUAL + WATCHLIST  -->
          <!-- ========================================== -->
          <tr>
            <td style="padding-bottom: 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>

                  <!-- LEFT COLUMN (49%): NEO-BRUTALIST PAYMENT CARD MOCKUP -->
                  <td width="49%" valign="top" style="background-color: #ffffff; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413; padding: 24px;">
                    <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; color: #52524e;">
                      Payment Instrument
                    </div>
                    <div style="font-size: 20px; font-weight: 900; color: #141413; margin-bottom: 16px;">
                      Flagged Card Profile
                    </div>

                    <!-- Stylized Physical Card Box -->
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5c542; border-top: 2px solid #141413; border-left: 2px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413; padding: 18px 20px; margin-bottom: 18px;">
                      <tr>
                        <td align="left" valign="top">
                          <div style="font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.8px; color: #141413;">
                            Card Ending In
                          </div>
                          <div style="font-size: 20px; font-weight: 900; font-family: monospace; color: #141413; letter-spacing: 1.5px; margin-top: 2px;">
                            &bull;&bull;&bull;&bull; &bull;&bull;&bull;&bull; &bull;&bull;&bull;&bull; {alert_data['card_number_masked']}
                          </div>
                        </td>
                        <td align="right" valign="top">
                          <span style="display: inline-block; background-color: #141413; color: #ffffff; font-size: 10px; font-weight: 900; text-transform: uppercase; padding: 3px 8px;">
                            {alert_data['transaction_status']}
                          </span>
                        </td>
                      </tr>
                      <tr>
                        <td colspan="2" style="padding-top: 16px;">
                          <div style="font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.8px; color: #141413;">
                            Attempted Amount
                          </div>
                          <div style="font-size: 26px; font-weight: 900; color: #141413; line-height: 1.1; margin-top: 2px;">
                            {alert_data['currency']} {amount:,.2f}
                          </div>
                        </td>
                      </tr>
                    </table>

                    <!-- Channel & Routing Mini-Grid -->
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border: 1.5px solid #141413; border-collapse: collapse;">
                      <tr style="background-color: #f9f9f8;">
                        <td style="padding: 10px 12px; font-size: 12px; font-weight: 700; color: #52524e; border-bottom: 1px solid #d6d3cd; border-right: 1px solid #d6d3cd;">
                          Transaction Type
                        </td>
                        <td align="right" style="padding: 10px 12px; font-size: 12px; font-weight: 900; color: #141413; border-bottom: 1px solid #d6d3cd;">
                          {alert_data['transaction_type']}
                        </td>
                      </tr>
                      <tr style="background-color: #ffffff;">
                        <td style="padding: 10px 12px; font-size: 12px; font-weight: 700; color: #52524e; border-bottom: 1px solid #d6d3cd; border-right: 1px solid #d6d3cd;">
                          Payment Channel
                        </td>
                        <td align="right" style="padding: 10px 12px; font-size: 12px; font-weight: 900; color: #141413; border-bottom: 1px solid #d6d3cd;">
                          {alert_data['payment_channel']}
                        </td>
                      </tr>
                      <tr style="background-color: #f9f9f8;">
                        <td style="padding: 10px 12px; font-size: 12px; font-weight: 700; color: #52524e; border-right: 1px solid #d6d3cd;">
                          International Routing
                        </td>
                        <td align="right" style="padding: 10px 12px; font-size: 12px; font-weight: 900; color: #141413;">
                          {intl_label}
                        </td>
                      </tr>
                    </table>
                  </td>

                  <!-- Spacer -->
                  <td width="2%">&nbsp;</td>

                  <!-- RIGHT COLUMN (49%): WATCHLIST INTELLIGENCE DOSSIER -->
                  <td width="49%" valign="top" style="background-color: #ffffff; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413; padding: 24px;">
                    <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; color: #52524e;">
                      Threat Intelligence
                    </div>
                    <div style="font-size: 20px; font-weight: 900; color: #141413; margin-bottom: 16px;">
                      Watchlist Record File
                    </div>

                    <!-- Watchlist ID Banner -->
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #141413; color: #ffffff; padding: 14px 16px; margin-bottom: 18px; border-left: 6px solid #ff5c5c;">
                      <tr>
                        <td align="left" valign="middle">
                          <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px; color: #a3a39e;">
                            Watchlist Reference ID
                          </div>
                          <div style="font-size: 18px; font-weight: 900; font-family: monospace; color: #f5c542; margin-top: 2px;">
                            {alert_data['watchlist_id']}
                          </div>
                        </td>
                        <td align="right" valign="middle">
                          <span style="display: inline-block; background-color: #262625; color: #ffffff; font-size: 11px; font-weight: 800; padding: 3px 8px; border: 1px solid #52524e;">
                            ACTIVE RECORD
                          </span>
                        </td>
                      </tr>
                    </table>

                    <!-- Watchlist Metadata Table -->
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border: 1.5px solid #141413; border-collapse: collapse;">
                      <tr style="background-color: #f9f9f8;">
                        <td style="padding: 12px 14px; font-size: 12px; font-weight: 700; color: #52524e; border-bottom: 1px solid #d6d3cd; width: 42%;">
                          Reported By
                        </td>
                        <td align="right" style="padding: 12px 14px; font-size: 13px; font-weight: 900; color: #141413; border-bottom: 1px solid #d6d3cd;">
                          {alert_data['reported_by']}
                        </td>
                      </tr>
                      <tr style="background-color: #ffffff;">
                        <td style="padding: 12px 14px; font-size: 12px; font-weight: 700; color: #52524e; border-bottom: 1px solid #d6d3cd;">
                          Reported Source
                        </td>
                        <td align="right" style="padding: 12px 14px; font-size: 13px; font-weight: 900; color: #141413; border-bottom: 1px solid #d6d3cd;">
                          {alert_data['reported_source']}
                        </td>
                      </tr>
                      <tr style="background-color: #f9f9f8;">
                        <td style="padding: 12px 14px; font-size: 12px; font-weight: 700; color: #52524e; border-bottom: 1px solid #d6d3cd;">
                          Watchlist Location
                        </td>
                        <td align="right" style="padding: 12px 14px; font-size: 13px; font-weight: 900; color: #141413; border-bottom: 1px solid #d6d3cd;">
                          {alert_data['watchlist_city']}, {alert_data['watchlist_country']}
                        </td>
                      </tr>
                      <tr style="background-color: #ffffff;">
                        <td style="padding: 12px 14px; font-size: 12px; font-weight: 700; color: #52524e;">
                          Effective From
                        </td>
                        <td align="right" style="padding: 12px 14px; font-size: 12px; font-weight: 900; font-family: monospace; color: #141413;">
                          {alert_data['watchlist_effective_from']}
                        </td>
                      </tr>
                    </table>
                  </td>

                </tr>
              </table>
            </td>
          </tr>

          <!-- ========================================== -->
          <!-- 4. 4-COLUMN TRANSACTION TELEMETRY STRIP    -->
          <!-- ========================================== -->
          <tr>
            <td style="padding-bottom: 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413;">
                <tr style="background-color: #141413; color: #ffffff;">
                  <td colspan="4" style="padding: 10px 20px; font-size: 12px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.8px; color: #f5c542;">
                    Transaction Event Telemetry
                  </td>
                </tr>
                <tr>
                  <td width="25%" valign="top" style="padding: 16px 18px; border-right: 1.5px solid #141413; background-color: #f9f9f8;">
                    <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: #52524e; letter-spacing: 0.6px;">
                      Transaction ID
                    </div>
                    <div style="font-size: 14px; font-weight: 900; font-family: monospace; color: #141413; margin-top: 4px;">
                      {alert_data['transaction_id']}
                    </div>
                  </td>
                  <td width="28%" valign="top" style="padding: 16px 18px; border-right: 1.5px solid #141413; background-color: #ffffff;">
                    <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: #52524e; letter-spacing: 0.6px;">
                      Merchant &amp; Category
                    </div>
                    <div style="font-size: 14px; font-weight: 900; color: #141413; margin-top: 4px;">
                      {alert_data['merchant_name']}
                    </div>
                    <div style="font-size: 11px; font-weight: 700; color: #52524e;">
                      {alert_data['merchant_category']}
                    </div>
                  </td>
                  <td width="24%" valign="top" style="padding: 16px 18px; border-right: 1.5px solid #141413; background-color: #f9f9f8;">
                    <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: #52524e; letter-spacing: 0.6px;">
                      Transaction Location
                    </div>
                    <div style="font-size: 14px; font-weight: 900; color: #141413; margin-top: 4px;">
                      {alert_data['transaction_city']}, {alert_data['transaction_country']}
                    </div>
                  </td>
                  <td width="23%" valign="top" style="padding: 16px 18px; background-color: #ffffff;">
                    <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: #52524e; letter-spacing: 0.6px;">
                      Event Timestamp
                    </div>
                    <div style="font-size: 13px; font-weight: 900; font-family: monospace; color: #141413; margin-top: 4px;">
                      {alert_data['transaction_timestamp']}
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- ========================================== -->
          <!-- 5. DUAL-PATH IMMEDIATE ACTION PROTOCOL     -->
          <!-- ========================================== -->
          <tr>
            <td style="padding-bottom: 28px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>

                  <!-- PATH A: UNAUTHORIZED ACTIVITY -->
                  <td width="49%" valign="top" style="background-color: #fff5f5; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413; padding: 22px;">
                    <div style="display: inline-block; background-color: #ff5c5c; color: #141413; font-size: 11px; font-weight: 900; text-transform: uppercase; padding: 3px 10px; border: 1.5px solid #141413; margin-bottom: 10px;">
                      If You Did NOT Authorize This
                    </div>
                    <div style="font-size: 18px; font-weight: 900; color: #141413; margin-bottom: 12px;">
                      Lock &amp; Report Immediately
                    </div>
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="font-size: 13px; line-height: 1.6; color: #141413; font-weight: 700;">
                      <tr>
                        <td valign="top" width="18" style="padding-bottom: 6px;">&bull;</td>
                        <td style="padding-bottom: 6px;">Call our Fraud Desk immediately at <span style="background-color: #ffffff; padding: 1px 6px; border: 1px solid #141413; font-family: monospace; font-weight: 900;">1-800-FRAUD-HELP</span></td>
                      </tr>
                      <tr>
                        <td valign="top" width="18" style="padding-bottom: 6px;">&bull;</td>
                        <td style="padding-bottom: 6px;">Your card has been flagged for priority security review</td>
                      </tr>
                      <tr>
                        <td valign="top" width="18">&bull;</td>
                        <td>Do not use this card until you speak with our security team</td>
                      </tr>
                    </table>
                  </td>

                  <!-- Spacer -->
                  <td width="2%">&nbsp;</td>

                  <!-- PATH B: AUTHORIZED ACTIVITY -->
                  <td width="49%" valign="top" style="background-color: #fefce8; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413; padding: 22px;">
                    <div style="display: inline-block; background-color: #f5c542; color: #141413; font-size: 11px; font-weight: 900; text-transform: uppercase; padding: 3px 10px; border: 1.5px solid #141413; margin-bottom: 10px;">
                      If You DID Authorize This
                    </div>
                    <div style="font-size: 18px; font-weight: 900; color: #141413; margin-bottom: 12px;">
                      Confirm &amp; Clear Alert
                    </div>
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="font-size: 13px; line-height: 1.6; color: #141413; font-weight: 700;">
                      <tr>
                        <td valign="top" width="18" style="padding-bottom: 6px;">&bull;</td>
                        <td style="padding-bottom: 6px;">Reply directly to this notification or call support to confirm the charge</td>
                      </tr>
                      <tr>
                        <td valign="top" width="18" style="padding-bottom: 6px;">&bull;</td>
                        <td style="padding-bottom: 6px;">Be prepared to complete a quick identity verification check</td>
                      </tr>
                      <tr>
                        <td valign="top" width="18">&bull;</td>
                        <td>Reference Case ID <span style="background-color: #ffffff; padding: 1px 6px; border: 1px solid #141413; font-family: monospace; font-weight: 900;">{alert_data['alert_id']}</span> for faster clearance</td>
                      </tr>
                    </table>
                  </td>

                </tr>
              </table>
            </td>
          </tr>

          <!-- ========================================== -->
          <!-- 6. NEO-BRUTALIST FOOTER BAR                -->
          <!-- ========================================== -->
          <tr>
            <td style="background-color: #f9f9f8; border-top: 1.5px solid #141413; border-left: 1.5px solid #141413; border-right: 4px solid #141413; border-bottom: 4px solid #141413; padding: 18px 24px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle" style="font-size: 12px; font-weight: 700; color: #52524e; line-height: 1.5;">
                    <strong style="color: #141413;">FinGuard Transaction Monitoring System</strong> &bull; Automated Fraud Watchlist Notification<br>
                    Your account security is our top priority. Never share your confidential card details with anyone.
                  </td>
                  <td align="right" valign="middle" style="font-size: 11px; font-family: monospace; font-weight: 800; color: #141413; white-space: nowrap; padding-left: 16px;">
                    ALERT ID: {alert_data['alert_id']}<br>
                    <span style="color: #52524e;">LOGGED: {alert_data['alert_timestamp']}</span>
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


@dp.foreach_batch_sink(name="fraud_email_notifier_sink")
def send_fraud_alert_emails(df, batch_id):
    """ForEachBatch sink that sends email alerts for fraud card transactions."""
    
    if APP_PASSWORD is None:
        print(f"❌ Batch {batch_id}: Gmail API key not available, skipping email notifications")
        return
    
    rows = df.collect()
    print(f"🚨 Batch {batch_id}: Processing {len(rows)} fraud alert(s)...")
    
    success_count = 0
    failure_count = 0
    
    for row in rows:
        try:
            # Mask card number (show only last 4 digits)
            card_number_masked = str(row.card_number)[-4:] if row.card_number else "****"
            
            alert_data = {
                'alert_id': row.alert_id,
                'alert_type': row.alert_type,
                'alert_timestamp': str(row.alert_timestamp),
                'customer_name': row.customer_name,
                'transaction_id': row.transaction_id,
                'card_number_masked': card_number_masked,
                'amount': float(row.amount),
                'currency': row.currency,
                'merchant_name': row.merchant_name,
                'merchant_category': row.merchant_category,
                'transaction_type': row.transaction_type,
                'payment_channel': row.payment_channel,
                'transaction_city': row.transaction_city,
                'transaction_country': row.transaction_country,
                'transaction_timestamp': str(row.transaction_timestamp),
                'is_international': row.is_international,
                'transaction_status': row.transaction_status,
                'watchlist_id': row.watchlist_id,
                'watch_type': row.watch_type,
                'risk_level': row.risk_level,
                'action': row.action,
                'reason_description': row.reason_description,
                'reported_by': row.reported_by,
                'reported_source': row.reported_source,
                'watchlist_city': row.watchlist_city if row.watchlist_city else 'N/A',
                'watchlist_country': row.watchlist_country if row.watchlist_country else 'N/A',
                'watchlist_effective_from': str(row.watchlist_effective_from)
            }
            
            subject = f"🚨 FRAUD ALERT - {alert_data['risk_level']} Risk - {alert_data['alert_id']}"
            body = create_fraud_alert_email_body(alert_data)
            
            send_email(row.customer_email, subject, body, EMAIL_FROM, APP_PASSWORD)
            
            success_count += 1
            print(f"  ✅ Fraud alert email sent to {row.customer_email} for transaction {row.transaction_id}")
            
        except Exception as e:
            failure_count += 1
            print(f"  ❌ Error processing fraud alert {row.alert_id}: {e}")
    
    print(f"📊 Batch {batch_id} complete: {success_count} succeeded, {failure_count} failed")


@dp.append_flow(target="fraud_email_notifier_sink")
def fraud_card_alert_stream():
    """Streaming flow that reads fraud card alerts."""
    return spark.readStream.table("fineguard.gold.fraud_card_alert")
