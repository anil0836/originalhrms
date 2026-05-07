import frappe

@frappe.whitelist()
def send_bulk_email(docname):
    doc = frappe.get_doc("Email Campaign", docname)

    if doc.email_campaign_for != "Email Group":
        frappe.throw("Please select Email Group for bulk sending")

    # Get emails
    members = frappe.get_all(
        "Email Group Member",
        filters={"email_group": doc.recipient},
        fields=["email"]
    )

    email_list = [m.email for m in members if m.email]

    if not email_list:
        frappe.throw("No emails found in selected Email Group")

    # ✅ FIX: use campaign_name (not campaign)
    campaign = frappe.get_doc("Campaign", doc.campaign_name)

    if not campaign.campaign_schedules:
        frappe.throw("No Email Template found in Campaign")

    template_name = campaign.campaign_schedules[0].email_template
    template = frappe.get_doc("Email Template", template_name)

    # Send emails
    frappe.sendmail(
        recipients=email_list,
        subject=template.subject or "No Subject",
        message=template.response or "No Message",
        now=False
    )

    return f"{len(email_list)} emails queued successfully"

